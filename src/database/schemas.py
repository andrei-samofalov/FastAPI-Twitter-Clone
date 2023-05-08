from typing import Optional

from pydantic import BaseModel, Field


class FollowUserOut(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class UserOut(FollowUserOut):
    followers: Optional[list[FollowUserOut]] = []
    following: Optional[list[FollowUserOut]] = []

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
