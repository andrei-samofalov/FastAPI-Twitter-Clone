"""
This module contains routes for router `media`
"""

from fastapi import APIRouter, Form, Response

router = APIRouter(prefix='/api/medias', tags=['media'])


@router.post('/')
async def upload_files(file: Form):
    """
    upload given file
    validate and return id
    don't forget to get url
    """
    return Response(status_code=200)
