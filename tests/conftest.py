import asyncio

import pytest
import json

from httpx import AsyncClient
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from database.init_db import db
from database.models import Base, Tweet, User
from database.schemas import TweetIn

from main import app

test_engine = create_async_engine(
    "postgresql+asyncpg://test:test@localhost:5433/test",
    echo=False,
    poolclass=NullPool,
)
TestSession = async_sessionmaker(
    bind=test_engine, expire_on_commit=False, class_=AsyncSession
)
Base.metadata.bind = test_engine

sync_engine = create_engine("postgresql://test:test@localhost:5433/test")
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


@pytest.fixture(autouse=True, scope="module")
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
            headers={"api_key": "test"}
    ) as cl:
        yield cl


@pytest.fixture(scope="session")
async def async_session():
    session = TestSession()
    try:
        yield session
    finally:
        await session.close()


@pytest.fixture(scope='module')
def user():
    return User(
        id=1,
        name='test',
        api_key='test'
    )


@pytest.fixture(scope='module')
def tweet():
    return TweetIn(
        tweet_data="hello world",
        tweet_media_ids=[]
    )
