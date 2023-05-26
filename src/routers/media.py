"""
This module contains routes for router `media`
"""
from fastapi import APIRouter, Depends, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from database.init_db import db
from schemas.media_schema import MediaOut
from utils.service import Dal

router = APIRouter(prefix='/medias', tags=['media'], redirect_slashes=False)


@router.post('', response_model=MediaOut, status_code=201)
async def upload_files(
    file: UploadFile,
    sess: AsyncSession = Depends(db),
):
    """
    upload given file
    validate and return id
    don't forget to get url
    """

    if not file:
        return {"message": "No upload file sent"}

    return await Dal(sess).upload_file(file)
