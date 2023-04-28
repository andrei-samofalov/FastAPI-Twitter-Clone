from typing import Optional

from pydantic import BaseModel, Field


class UserIn(BaseModel):
    name: str


class FollowUserOut(UserIn):
    id: int

    class Config:
        orm_mode = True


class UserOut(FollowUserOut):
    result: True
    followers: Optional[list[FollowUserOut]] = []
    following: Optional[list[FollowUserOut]] = []


class TweetIn(BaseModel):
    tweet_data: str
    tweet_media_ids: Optional[list[int]]


class TweetOut(BaseModel):
    tweet_id: int

    class Config:
        orm_mode = True
