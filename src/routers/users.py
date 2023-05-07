"""
This module contains routes for router `tweets`
"""

from typing import Annotated

from fastapi import APIRouter, Header, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from loguru import logger

from database.service import Dal
from database.models import User
from database.init_db import db
from database.schemas import UserResponse

router = APIRouter(prefix='/api/users', tags=['users'])


@router.get('/me', response_model=UserResponse)
async def get_user(
        sess: AsyncSession = Depends(db),
        api_key: Annotated[str | None, Header()] = None
):
    """get account details"""
    stmt = select(User).filter_by(api_key=api_key)

    current_user: User = await sess.scalar(stmt)

    logger.debug(f'{current_user=}')
    return {
        "result": True,
        "user": current_user
    }


@router.get('/{idx}', response_model=UserResponse)
async def get_user_by_id(
        idx: int,
        sess: AsyncSession = Depends(db),
        api_key: Annotated[str | None, Header()] = None
):
    """return specific user data"""
    stmt = select(User).filter_by(id=idx)

    current_user: User = await sess.scalar(stmt)

    logger.debug(f'{current_user=}')

    return {
        "result": True,
        "user": current_user
    }


@router.post('/{idx}/follow')
async def follow_user(
        idx: int,
        sess: AsyncSession = Depends(db),
        api_key: Annotated[str | None, Header()] = None
):
    """follow specific user"""
    stmt = select(User).filter_by(api_key=api_key)

    current_user: User = await sess.scalar(stmt)

    logger.debug(f'{current_user=}')

    stmt2 = select(User).filter_by(id=idx)
    user_for_follow: User = await sess.scalar(stmt2)

    current_user.following = user_for_follow
    await sess.commit()

    return {'result': True}


@router.delete('/{idx}/follow')
async def unfollow_user(idx: int):
    """unfollow specific user"""
