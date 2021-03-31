from typing import Union, Optional
from src.message_server.utils.depends import AuthenticationError
from src import models, schemas
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload


async def get_user_by_auth(
    email: str,
    password: str,
    session: AsyncSession,
    throw: bool = True,
    all_channels=False,
) -> Optional[Union[schemas.UserInternal, schemas.UserInternalWithChannels]]:
    if all_channels:
        stmt = (
            select(models.User)
            .filter(models.User.email == email, models.User.password == password)
            .options(selectinload(models.User.owned_channels))
            .options(selectinload(models.User.memberships))
        )
        schema = schemas.UserInternalWithChannels
    else:
        stmt = (
            select(models.User)
            .filter(models.User.email == email, models.User.password == password)
            .options(selectinload(models.User.owned_channels))
        )
        schema = schemas.UserInternal
    results = await session.execute(stmt)
    result = results.scalars().first()
    if result is None:
        if throw:
            raise AuthenticationError("No matching user found")
        else:
            return None
    return schema.from_orm(result)


async def get_user_by_name_and_hash(
    name: str, hash: str, session: AsyncSession
) -> Optional[schemas.UserInternal]:
    stmt = (
        select(models.User)
        .filter(models.User.name == name, models.User.hash == hash)
        .options(selectinload(models.User.owned_channels))
    )
    results = await session.execute(stmt)
    result = results.scalars().first()
    if result is None:
        return None
    return schemas.UserInternal.from_orm(result)
