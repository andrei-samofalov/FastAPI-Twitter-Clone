from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from utils.settings import get_db_url

url = get_db_url()
async_engine = create_async_engine(
    url,
    # echo=True
)
Session = async_sessionmaker(
    bind=async_engine, expire_on_commit=False, class_=AsyncSession
)


async def db():  # noqa
    async with Session() as session:
        yield session
