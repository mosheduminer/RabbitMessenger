from typing import Optional
from src import models, schemas
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update, delete


async def get_channel_by_uuid(
    uuid: str, session: AsyncSession
) -> Optional[schemas.Channel]:
    stmt = select(models.Channel).filter(models.Channel.id == uuid)
    result = (await session.execute(stmt)).scalars().first()
    if result is None:
        return None
    return schemas.Channel.from_orm(result)


async def new_group_channel(owner_id: int, name: str, session: AsyncSession) -> str:
    channel = models.Channel(
        name=name, type=models.ChannelType.GROUP, owner_id=owner_id
    )
    async with session.begin():
        session.add(channel)
    return channel.id


async def remove_group_channel(channel_id: str, session: AsyncSession) -> str:
    stmt = delete(models.Channel).where(models.Channel.id == channel_id)
    await session.execute(stmt)


async def modify_group_channel_name(
    channel_id: str, new_name: str, session: AsyncSession
):
    stmt = (
        update(models.Channel)
        .where(models.Channel.id == channel_id)
        .values(name=new_name)
    )
    await session.execute(stmt)


async def get_user(
    name: str, hash: str, session: AsyncSession
) -> Optional[models.User]:
    stmt = select(models.User).filter(
        models.User.name == name, models.User.hash == hash
    )
    return (await session.execute(stmt)).scalars().first()


async def add_user_to_group_channel(
    channel_id: str, user_name: str, user_hash: str, session: AsyncSession
):
    user = await get_user(user_name, user_hash, session)
    if user is None:
        return False
    async with session.begin():
        session.add(models.Membership(user_id=user.id, channel_id=channel_id))
    return True


async def delete_user_from_group_channel(
    channel_id: str, user_name: str, user_hash: str, session: AsyncSession
):
    user = await get_user(user_name, user_hash, session)
    if user is None:
        return False
    stmt = delete(models.Membership).where(
        models.Membership.channel_id == channel_id, models.Membership.user_id == user.id
    )
    await session.execute(stmt)
    return True
