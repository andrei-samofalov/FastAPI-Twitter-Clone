"""
This module contains routes for router `tweets`
"""

from typing import Annotated

from fastapi import APIRouter, Header, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, and_

from loguru import logger

from database.service import Dal
from database.models import User, UserToUser
from database.init_db import db
from database.schemas import UserResponse

router = APIRouter(prefix='/api/users', tags=['users'])


@router.get('/me')
async def get_user(
    sess: AsyncSession = Depends(db),
    api_key: Annotated[str | None, Header()] = None,
):
    """Get current user account details."""
    user = await Dal(sess).get_current_user(api_key)
    return {"result": True, "user": user}


@router.get('/{idx}')
async def get_user_by_id(idx: int, sess: AsyncSession = Depends(db)):
    """Get specific user details."""
    user = await Dal(sess).get_user_by_idx(idx)
    return {"result": True, "user": user}


@router.post('/{idx}/follow')
async def follow_user(
    idx: int,
    sess: AsyncSession = Depends(db),
    api_key: Annotated[str | None, Header()] = None,
):
    """follow specific user"""
    current_user: User = await Dal(sess).get_current_user(api_key)
    user_for_follow: User = await Dal(sess).get_user_by_idx(idx)

    async with sess.begin():
        current_user.following = user_for_follow

    return {'result': True}


@router.delete('/{idx}/follow')
async def unfollow_user(
    idx: int,
    sess: AsyncSession = Depends(db),
    api_key: Annotated[str | None, Header()] = None,
):
    """Unfollow specific user."""
    current_user: User = await Dal(sess).get_current_user(api_key)
    user_for_follow: User = await Dal(sess).get_user_by_idx(idx)

    async with sess.begin():
        # potential exc
        stmt = delete(UserToUser).filter(
            and_(
                UserToUser.slave_id == current_user.id,
                UserToUser.master_id == user_for_follow.id
            )
        )
        await sess.execute(stmt)

    return {'result': True}
