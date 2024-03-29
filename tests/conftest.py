import asyncio
import json

import pytest
from httpx import AsyncClient
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from database.init_db import db
from database.models import Base, User, Tweet
from main import app
from utils.settings import get_settings

s = get_settings()

test_engine = create_async_engine(
    s.test_db,
    echo=False,
    poolclass=NullPool,
)
TestSession = async_sessionmaker(
    bind=test_engine, expire_on_commit=False, class_=AsyncSession
)
Base.metadata.bind = test_engine

sync_engine = create_engine("postgresql://admin:admin@localhost:5433/test")
SyncSession = sessionmaker(bind=sync_engine)


async def override_db():
    session = TestSession()
    try:
        yield session
    finally:
        await session.close()


app.dependency_overrides[db] = override_db


@pytest.fixture(scope="session")
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(autouse=True, scope="session")
async def startup(async_session):
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="session")
async def async_client():
    async with AsyncClient(
            app=app,
            base_url="http://localhost:5000",
            headers={"api-key": "test"}
    ) as cl:
        yield cl


@pytest.fixture(scope="session")
async def async_session():
    async with TestSession() as session:
        yield session


@pytest.fixture(scope='class')
def user_1():
    return User(
        id=1,
        name='test',
        api_key='test'
    )


@pytest.fixture(scope='class')
def user_1_expected():
    return {
        "result": True,
        "user": {"id": 1, "name": "test", "following": [], "followers": []}
    }


@pytest.fixture(scope='class')
def user_2():
    return User(
        id=2,
        name='test2',
        api_key='test2'
    )


@pytest.fixture(scope='class')
def user_2_expected():
    return {
        "result": True,
        "user": {"id": 1, "name": "test2", "following": [], "followers": []}
    }


@pytest.fixture(scope='session')
def tweet():
    return json.dumps(dict(
        tweet_data="hello world",
        tweet_media_ids=[])
    )


@pytest.fixture(scope='class')
def tweetDB_us1():
    return Tweet(
        # id=1,
        content="test_tweet",
        user_id=1
    )
