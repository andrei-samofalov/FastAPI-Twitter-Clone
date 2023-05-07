"""
This module contains routes for router `tweets`
"""

from typing import Annotated

from fastapi import APIRouter, Header, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, and_

from loguru import logger

from database.service import Dal, get_current_user, get_user_by_idx
from database.models import User, follows
from database.init_db import db
from database.schemas import UserResponse

router = APIRouter(prefix='/api/users', tags=['users'])


@router.get('/me')
async def get_user(
        sess: AsyncSession = Depends(db),
        api_key: Annotated[str | None, Header()] = None
):
    """Get current user account details."""
    user = await get_current_user(api_key, sess)
    return {"result": True, "user": user}


@router.get('/{idx}')
async def get_user_by_id(idx: int, sess: AsyncSession = Depends(db)):
    """Get specific user details."""
    user = await get_user_by_idx(idx, sess)
    return {"result": True, "user": user}


@router.post('/{idx}/follow')
async def follow_user(
        idx: int,
        sess: AsyncSession = Depends(db),
        api_key: Annotated[str | None, Header()] = None
):
    """follow specific user"""
    current_user: User = await get_current_user(api_key, sess)
    user_for_follow: User = await get_user_by_idx(idx, sess)

    async with sess.begin():
        current_user.following = user_for_follow

    return {'result': True}


@router.delete('/{idx}/follow')
async def unfollow_user(
        idx: int,
        sess: AsyncSession = Depends(db),
        api_key: Annotated[str | None, Header()] = None
):
    """unfollow specific user"""
    current_user: User = await get_current_user(api_key, sess)
    user_for_follow: User = await get_user_by_idx(idx, sess)

    async with sess.begin():
        stmt = delete(follows).filter(
            and_(
                follows.c.follower_id == current_user.id,
                follows.c.following_id == user_for_follow.id
            )
        )
        await sess.execute(stmt)

    return {'result': True}
