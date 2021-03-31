import asyncio
from src.security import get_user_by_name_and_hash
from .database import (
    add_user_to_group_channel,
    delete_user_from_group_channel,
    get_channel_by_uuid,
    get_user,
    modify_group_channel_name,
    new_group_channel,
    remove_group_channel,
)
from aio_pika.robust_connection import RobustConnection
from sqlalchemy.ext.asyncio import AsyncSession
from websockets import WebSocketServerProtocol
import logging

from .queue import (
    create_connection,
    QueueConnection,
    queue_message_subscribe,
    send_message_to_queue,
)
from .utils import Router, Depends, StatusError
from .security import authenticate_user, authenticate_user_with_channels
from ..database import Session
from .. import schemas
from uuid import UUID
import websockets

app = Router((Depends(authenticate_user),))

logger = logging.getLogger("message-server")


@app.route("user-info", deps=(Depends(authenticate_user),))
async def user_info(
    name: str,
    hash: str,
    session: AsyncSession = Depends(Session),
):
    user = await get_user(name, hash, session)
    return schemas.UserExternal.from_orm(user).json()


@app.route("send-group-message")
async def send_message(
    message: schemas.SendGroupMessage,
    session: AsyncSession = Depends(Session),
    queue_connection: RobustConnection = Depends(QueueConnection),
):
    uuid = UUID(message.channel_uuid)
    if await get_channel_by_uuid(uuid.hex, session) is not None:
        await send_message_to_queue(
            queue_connection, uuid.hex, message.message.encode()
        )
        return True
    raise StatusError(404, "send-group-message", "channel not found")


@app.route("send-user-message")
async def send_message(
    message: schemas.SendUserMessage,
    session: AsyncSession = Depends(Session),
    queue_connection: RobustConnection = Depends(QueueConnection),
):
    if await get_user_by_name_and_hash(message.name, message.hash, session) is not None:
        await send_message_to_queue(
            queue_connection,
            f"{message.name}#{message.hash}",
            message.message.encode(),
        )
        return True
    raise StatusError(404, "send-user-message", "user not found")


@app.route("subscribe-for-messages")
async def listen_for_messages(
    ws: WebSocketServerProtocol,
    user: schemas.UserInternalWithChannels = Depends(authenticate_user_with_channels),
    queue_connection: RobustConnection = Depends(QueueConnection),
):
    listen_personal_task = asyncio.create_task(
        queue_message_subscribe(queue_connection, f"{user.name}#{user.hash}", ws)
    )
    group_ids = [membership.id for membership in user.memberships] + [
        channel.id.hex for channel in user.owned_channels
    ]
    # TODO cancel a specific task when a user is removed from a channel
    listen_group_tasks = {
        group_id: asyncio.create_task(
            queue_message_subscribe(queue_connection, group_id, ws)
        )
        for group_id in group_ids
    }
    while True:
        await asyncio.sleep(3)
        try:
            await ws.ensure_open()
        except websockets.exceptions.ConnectionClosed:
            listen_personal_task.cancel()
            for task in listen_group_tasks.values():
                task.cancel()
            await listen_personal_task
            await asyncio.gather(listen_group_tasks.values())


@app.route("create-group-channel")
async def create_group_channel(
    name: str,
    session: AsyncSession = Depends(Session),
    user: schemas.UserInternal = Depends(authenticate_user),
):
    return await new_group_channel(user.id, name, session)


@app.route("delete-group-channel")
async def delete_group_channel(
    channel_id: str,
    session: AsyncSession = Depends(Session),
    user: schemas.UserInternal = Depends(authenticate_user),
):
    if channel_id in (channel.id for channel in user.owned_channels):
        await remove_group_channel(channel_id, session)
        return True
    raise StatusError(
        404,
        "delete-group-channel",
        "this user does not own a channel with the given ID",
    )


@app.route("change-group-channel-name")
async def change_group_channel_name(
    name: str,
    channel_id: str,
    session: AsyncSession = Depends(Session),
    user: schemas.UserInternal = Depends(authenticate_user),
):
    if channel_id in (channel.id for channel in user.owned_channels):
        await modify_group_channel_name(channel_id, name, session)
        return True
    raise StatusError(
        404,
        "change-group-channel-name",
        "this user does not own a channel with the given ID",
    )


@app.route("add-user-to-channel")
async def add_user_to_channel(
    name: str,
    hash: str,
    channel_id: str,
    session: AsyncSession = Depends(Session),
    user: schemas.UserInternal = Depends(authenticate_user),
):
    if channel_id in (channel.id for channel in user.owned_channels):
        return await add_user_to_group_channel(channel_id, name, hash, session)
    raise StatusError(
        404,
        "add-user-to-channel",
        "this user does not own a channel with the given ID",
    )


@app.route("remove-user-from-channel")
async def remove_user_from_channel(
    name: str,
    hash: str,
    channel_id: str,
    session: AsyncSession = Depends(Session),
    user: schemas.UserInternal = Depends(authenticate_user),
):
    if channel_id in (channel.id for channel in user.owned_channels):
        return await delete_user_from_group_channel(channel_id, name, hash, session)
    raise StatusError(
        404,
        "remove-user-from-channel",
        "this user does not own a channel with the given ID",
    )


def main():
    async def start_server():
        await create_connection()
        await websockets.serve(app, "localhost", 6789)

    logging.getLogger("router").setLevel(logging.DEBUG)
    logger.setLevel(logging.DEBUG)
    logging.basicConfig(
        format="%(levelname)s %(asctime)s - %(message)s", datefmt="%d-%b-%y %H:%M:%S"
    )
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(start_server())
        loop.run_forever()
    except KeyboardInterrupt:
        logger.debug("KeyboardInterrupt - exiting")


if __name__ == "__name__":
    main()
