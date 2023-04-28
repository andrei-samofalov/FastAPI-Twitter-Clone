import os

from dotenv import load_dotenv
from sqlalchemy import URL
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

load_dotenv()

db_url = URL.create(
    drivername="postgresql+asyncpg",
    username=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD"),
    host="db",
    port=5432,
    database="admin",
)

async_engine = create_async_engine(db_url, echo=True)
Session = async_sessionmaker(
    bind=async_engine, expire_on_commit=False, class_=AsyncSession
)


async def db():  # pragma: no cover
    session: AsyncSession = Session()
    try:
        yield session
    finally:
        await session.close()
