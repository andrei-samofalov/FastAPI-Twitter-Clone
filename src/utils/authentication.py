from fastapi import Depends, HTTPException, Security
from fastapi.security import APIKeyHeader
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from database.init_db import db
from utils.service import Dal

api_key = APIKeyHeader(name="api-key")


async def get_current_user(
    api_key_header: str = Security(api_key),
    session: AsyncSession = Depends(db),
):
    """Возвращает пользователя из базы данных по API ключу."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"api-key": ""},
    )
    user = await Dal(session).get_current_user(api_key_header)
    if user is None:
        raise credentials_exception
    return user
