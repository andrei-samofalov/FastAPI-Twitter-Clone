from typing import Optional

from pydantic import BaseModel, Field
from fastapi.openapi import utils


class CustomRequestValidationError(BaseModel):
    message: str
    type: str


validation_schema = CustomRequestValidationError.schema()

custom_validation_error_definition = dict(validation_schema)

validation_schema.update({"title": "HTTPValidationError"})

custom_validation_error_response_definition = dict(validation_schema)

utils.validation_error_definition = custom_validation_error_definition
utils.validation_error_response_definition = custom_validation_error_response_definition


class FollowUserOut(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class UserOut(FollowUserOut):
    followers: list[FollowUserOut] = []
    following: list[FollowUserOut] = []

    class Config:
        orm_mode = True


class UserResponse(FollowUserOut):
    result: bool = True
    user: UserOut

    class Config:
        orm_mode = True


class TweetIn(BaseModel):
    content: str = Field(..., alias='tweet_data')
    tweet_media_ids: Optional[list[int]] = []


class TweetOut(BaseModel):
    result: bool = True
    id: int = Field(...)

    class Config:
        orm_mode = True
