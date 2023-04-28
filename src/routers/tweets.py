"""
This module contains routes for router `tweets`
"""

from fastapi import APIRouter

router = APIRouter(prefix='/api/tweets', tags=['tweets'])


@router.get('/')
async def get_tweets():
    """get all tweets"""
    return {
        "result": 'True',
        "tweets": [
            {
                "id": 1,
                "content": "string",
                # "attachments": [
                # ],
                "author": {
                    "id": 1,
                    "name": "string"
                },
                "likes": [
                    {
                        "user_id": 1,
                        "name": "string"
                    }
                ]
            },
        ]
    }


@router.post('/')
async def add_tweet():
    """post new tweet"""
    pass


@router.delete('/{id}')
async def delete_tweet(id: int):
    """delete specific tweet"""
    pass


@router.post('/{id}/likes')
async def add_like_to_tweet(id: int):
    """add like to tweet"""
    pass


@router.delete('/{id}/likes')
async def remove_like_from_tweet(id: int):
    """remove like from tweet"""
    pass
