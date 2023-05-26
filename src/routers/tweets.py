"""
This module contains routes for router `tweets`
"""
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database.init_db import db
from database.models import User
from schemas.base_schema import BaseSchema
from schemas.tweet_schema import TweetIn, TweetOut, TweetsOut
from utils.authentication import get_current_user
from utils.responses import RESPONSE_401_422_404, RESPONSE_401_422_404_403
from utils.service import Dal

router = APIRouter(prefix='/tweets', tags=['tweets'])


@router.get('/', response_model=TweetsOut, status_code=200)
async def _get_tweets(
    current_user: Annotated[User, Depends(get_current_user)],
    sess: Annotated[AsyncSession, Depends(db)],
):
    """Get all tweets from current user and user's followee."""

    tweets = await Dal(sess).get_all_tweets(current_user)
    return {"tweets": tweets}


@router.post('/', response_model=TweetOut, status_code=201)
async def add_tweet(
    tweet: TweetIn,
    current_user: Annotated[User, Depends(get_current_user)],
    sess: Annotated[AsyncSession, Depends(db)],
):
    """Post new tweet."""

    return await Dal(sess).add_tweet(tweet=tweet, user_id=current_user.id)


@router.delete(
    '/{idx}',
    response_model=BaseSchema,
    responses=RESPONSE_401_422_404_403,
    status_code=200,
)
async def delete_tweet(
    idx: int,
    current_user: Annotated[User, Depends(get_current_user)],
    sess: Annotated[AsyncSession, Depends(db)],
):
    """Delete own specific tweet."""

    await Dal(sess).delete_tweet(tweet_id=idx, user_id=current_user.id)
    return {"result": True}


@router.post(
    '/{idx}/likes',
    response_model=BaseSchema,
    responses=RESPONSE_401_422_404,
    status_code=201,
)
async def add_like_to_tweet(
    idx: int,
    current_user: Annotated[User, Depends(get_current_user)],
    sess: Annotated[AsyncSession, Depends(db)],
):
    """Add like to tweet."""

    await Dal(sess).add_like_to_tweet(tweet_id=idx, user_id=current_user.id)
    return {'result': True}


@router.delete(
    '/{idx}/likes',
    response_model=BaseSchema,
    responses=RESPONSE_401_422_404,
    status_code=200,
)
async def remove_like_from_tweet(
    idx: int,
    current_user: Annotated[User, Depends(get_current_user)],
    sess: Annotated[AsyncSession, Depends(db)],
):
    """Remove like from tweet."""

    await Dal(sess).remove_like_from_tweet(
        tweet_id=idx, user_id=current_user.id
    )
    return {'result': True}
