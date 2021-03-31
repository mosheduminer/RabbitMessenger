from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy import MetaData
from sqlalchemy.orm import sessionmaker

# here as an export
from src.models import Base

from src import settings

engine = create_async_engine(settings.ASYNC_SQLALCHEMY_DATABASE_URL, future=True)

metadata = MetaData(engine)

maker = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def Session():
    try:
        session = maker()
        yield session
    finally:
        await session.close()
