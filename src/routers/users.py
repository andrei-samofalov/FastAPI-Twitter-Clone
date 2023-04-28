"""
This module contains routes for router `tweets`
"""

from fastapi import APIRouter

router = APIRouter(prefix='/api/users', tags=['users'])


@router.get('/me')
async def get_user():
    """get account details"""
    return {
        "result": "true",
        "user": {
            "id": 1,
            "name": "str",
            "followers": [
                {
                    "id": 2,
                    "name": "str"
                }
            ],
            "following": [
                {
                    "id": 2,
                    "name": "str"
                }
            ]
        }
    }


@router.get('/{id}')
async def get_user_by_id(id: int):
    """return specific user data"""
    return {
        "result": "true",
        "user": {
            "id": 1,
            "name": "str",
            "followers": [
                {
                    "id": 2,
                    "name": "str"
                }
            ],
            "following": [
                {
                    "id": 2,
                    "name": "str"
                },
                {
                    "id": 3,
                    "name": "str"
                }
            ]
        }
    }


@router.post('/{id}/follow')
async def follow_user(id: int):
    """follow specific user"""


@router.delete('/{id}/follow')
async def unfollow_user(id: int):
    """unfollow specific user"""
