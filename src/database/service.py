from datetime import datetime
from typing import Type, TypeVar

from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Base, User, Tweet, TweetMedia, follows

Model = TypeVar("Model", bound=Type[Base])
Schema = TypeVar("Schema", bound=BaseModel)


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
            raise HTTPException(status_code=404, detail="not found")

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

