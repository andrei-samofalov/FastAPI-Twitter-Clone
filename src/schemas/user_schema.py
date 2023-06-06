from typing import Optional

from pydantic import BaseModel, Field

from .base_schema import BaseSchema


class BaseUser(BaseModel):
    id: int
    name: Optional[str]

    class Config:
        orm_mode = True


class User(BaseUser):
    following: list[BaseUser]
    followers: list[BaseUser]

    class Config:
        orm_mode = True


class UserOut(BaseSchema):
    user: User
