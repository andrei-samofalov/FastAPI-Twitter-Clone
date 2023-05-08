"""
This module contains routes for router `tweets`
"""
from typing import Annotated

from fastapi import APIRouter, Depends, Header
from fastapi.requests import Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete

from loguru import logger

from database.init_db import db
from database.models import Tweet, User, TweetLike
from database.schemas import TweetIn, TweetOut
from database.service import Dal

router = APIRouter(prefix='/api/tweets', tags=['tweets'])


@router.get('/')
async def get_tweets(
        api_key: Annotated[str | None, Header()] = None,
        sess: AsyncSession = Depends(db)
):
    """Get all tweets from current user's followee."""

    tweets = await Dal(sess).get_all_tweets()
    logger.debug(f'{tweets=}')
    return {"result": True, "tweets": tweets}


@router.post('/', response_model=TweetOut, status_code=201)
async def add_tweet(
    tweet: TweetIn,
    api_key: Annotated[str | None, Header()] = None,
    sess: AsyncSession = Depends(db),
):
    """Post new tweet."""
    logger.debug(f"{tweet=}")
    logger.debug(f"{api_key=}")

    tweet_data = tweet.dict()

    curr_user = await Dal(sess).get_current_user(api_key)
    tweet_data.update({'user_id': curr_user.id})

    new_tweet = Tweet(**tweet_data)
    sess.add(new_tweet)
    await sess.commit()
    # return await Dal(sess).add_one(Tweet, tweet)
    return new_tweet


@router.delete('/{idx}')
async def delete_tweet(
    idx: int,
    api_key: Annotated[str | None, Header()] = None,
    sess: AsyncSession = Depends(db),
):
    """delete specific tweet"""
    # if tweet.user == api-key user
    pass


@router.post('/{idx}/likes')
async def add_like_to_tweet(
    idx: int,
    api_key: Annotated[str | None, Header()] = None,
    sess: AsyncSession = Depends(db),
):
    """add like to tweet"""

    stmt = select(User.id).filter_by(api_key=api_key)
    async with sess.begin():
        user_id = await sess.scalar(stmt)
        tweet = await sess.get(Tweet, idx)
        new_like = TweetLike(tweet_id=tweet.id, user_id=user_id)
        sess.add(new_like)
    # await sess.commit()
    return {'result': True}


@router.delete('/{idx}/likes')
async def remove_like_from_tweet(
    idx: int,
    api_key: Annotated[str | None, Header()] = None,
    sess: AsyncSession = Depends(db),
):
    """Remove like from tweet."""

    curr_user = await Dal(sess).get_current_user(api_key)
    async with sess.begin():
        curr_tweet = await sess.get(Tweet, idx)

    if curr_tweet.user_id == curr_user.id:
        stmt = delete(TweetLike).filter_by(user_id=curr_user.id)
        async with sess.begin():
            await sess.execute(stmt)

    return {'result': True}
