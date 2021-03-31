from src.security import get_user_by_auth
from src.message_server.utils.depends import AuthenticationError
from src.database import Session
from .utils import Depends
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.future import select
from websockets import WebSocketServerProtocol


async def authenticate_user(
    ws: WebSocketServerProtocol,
    session: AsyncSession = Depends(Session),
    # ret: bool = False,
    all_channels=False,
):
    auth = ws.request_headers.get("authorization")
    # for now, auth is just email:password

    if auth is None:
        raise AuthenticationError("authorization header not provided")
    segments = auth.split(":")
    if len(segments) != 2:
        raise AuthenticationError(
            "authorization header does not match scheme user:password"
        )
    password = segments.pop()
    email = "".join(segments)
    yield await get_user_by_auth(email, password, session, all_channels=all_channels)


async def authenticate_user_with_channels(
    ws: WebSocketServerProtocol,
    session: AsyncSession = Depends(Session),
):
    async for user in authenticate_user(ws, session, all_channels=True):
        yield user
