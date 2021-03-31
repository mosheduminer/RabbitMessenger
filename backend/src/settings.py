import os


DB_HOST = os.getenv("DB_HOST") or "localhost"
DB_PORT = os.getenv("DB_PORT") or "5432"
DB_USER = os.getenv("DB_USER") or "postgres"
DB_PASSWORD = os.getenv("DB_PASSWORD") or "123456"
DB_DATABASE = os.getenv("DB_DATABASE") or "RabbitMessenger"

ASYNC_SQLALCHEMY_DATABASE_URL = (
    f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_DATABASE}"
)

SYNC_SQLALCHEMY_DATABASE_URL = (
    f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_DATABASE}"
)
