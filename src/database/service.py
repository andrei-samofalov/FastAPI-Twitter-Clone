from datetime import datetime
from typing import Type, TypeVar

from loguru import logger
from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import joinedload, selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Base, User, Tweet, TweetMedia, UserToUser
from exceptions.HTTPExceptions import ApiError

Model = TypeVar("Model", bound=Type[Base])
Schema = TypeVar("Schema", bound=BaseModel)


async def get_user_followers(user: User, session: AsyncSession):
    async with session.begin():
        stmt = select(UserToUser.slave_id).where(
            UserToUser.master_id == user.id
        )
        followers = await session.scalars(stmt)

    return followers


async def _get_tweets(user: User, session: AsyncSession):
    """Return all tweets by following users"""

    followee = await get_user_followers(user, session)

    logger.debug(f'{user.following=}')
    q = (
        select(Tweet)
        .options(joinedload(User.following))
        .where(Tweet.user_id.in_(followee))
        .order_by(Tweet.likes)
    )
    async with session.begin():
        tweets = await session.scalars(q)

    return tweets


class Dal:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def _transform_schema_to_object(self, model: Model, schema: Schema):
        """create model object from given schema"""
        return model(**schema.dict())

    async def _check_obj(self, obj_type: Model, obj_id: int):
        """
        check if object in database,
        if so - return object, otherwise - raise HTTPException (not found)
        """
        async with self._session.begin():
            obj = await self._session.get(obj_type, obj_id)
        if not obj:
            class_name = obj_type.__class__.__name__
            raise ex.ApiError(
                status_code=404, detail="not found",
                error_type='database',
                error_message=f'{class_name} with id {obj_id} not found :('
            )

        return obj

    async def get_one(self, model: Model, idx: int) -> Model | None:
        """Return model object with given idx if it is in database."""
        return await self._check_obj(model, idx)

    async def add_one(self, model: Model, schema: Schema) -> Model:
        """Add given data to database, return new object."""
        new_obj = await self._transform_schema_to_object(model, schema)
        async with self._session.begin():
            self._session.add(new_obj)
        return new_obj

    async def _get_all(self, model: Model):
        """return all objects of given model"""
        async with self._session.begin():
            result = await self._session.scalars(select(model))

        return result.all()

    async def get_all_tweets(self):
        """Return all tweets"""
        return await self._get_all(Tweet)

    async def get_current_user(self, api_key: str) -> User:
        """Return current user by api key."""
        stmt = (
            select(User)
            .filter_by(api_key=api_key)
        )
        # TODO followers and following
        async with self._session.begin():
            # potential exc
            current_user: User = await self._session.scalar(stmt)

        return current_user

    async def get_user_by_idx(self, idx: int):
        """Return user by id."""
        return await self.get_one(User, idx)
