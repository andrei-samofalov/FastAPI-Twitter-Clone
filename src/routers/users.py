"""
This module contains routes for router `tweets`
"""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from database.init_db import db
from database.models import User
from schemas.base_schema import BaseSchema
from schemas.user_schema import UserOut

# from database.schemas import UserOut
from utils.authentication import get_current_user
from utils.responses import RESPONSE_401, RESPONSE_401_422_404, RESPONSE_401_422_404_400
from utils.service import Dal

router = APIRouter(prefix='/users', tags=['users'])


@router.get(
    '/me',
    # response_model=UserOut,
    responses=RESPONSE_401,
    status_code=200,
)
async def get_user(current_user: Annotated[User, Depends(get_current_user)]):
    """Получить информацию о текущем пользователе"""
    logger.debug(f'{current_user=}')
    return {"user": current_user}


@router.get(
    '/{idx}',
    response_model=UserOut,
    responses=RESPONSE_401_422_404,
    status_code=200,
)
async def get_user_by_id(idx: int, sess: AsyncSession = Depends(db)):
    """Get specific user details."""
    user: User = await Dal(sess).get_user_by_idx(idx)
    return {"user": user}


@router.post(
    '/{idx}/follow',
    response_model=BaseSchema,
    responses=RESPONSE_401_422_404_400,
    status_code=200,
)
async def follow_user(
    idx: int,
    current_user: Annotated[User, Depends(get_current_user)],
    sess: Annotated[AsyncSession, Depends(db)],
):
    """follow specific user"""
    user_for_follow: User = await Dal(sess).get_user_by_idx(idx)
    if user_for_follow.id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Can't follow yourself",
        )
    if user_for_follow not in current_user.following:
        async with sess.begin():
            current_user.following.append(user_for_follow)
            sess.add(current_user)

    return {'result': True}


@router.delete(
    '/{idx}/follow',
    response_model=BaseSchema,
    responses=RESPONSE_401_422_404,
    status_code=200,
)
async def unfollow_user(
    idx: int,
    current_user: Annotated[User, Depends(get_current_user)],
    sess: Annotated[AsyncSession, Depends(db)],
):
    """Unfollow specific user."""
    user_for_unfollow: User = await Dal(sess).get_user_by_idx(idx)
    if user_for_unfollow in current_user.following:
        async with sess.begin():
            current_user.following.remove(user_for_unfollow)
            sess.add(current_user)

    return {'result': True}
