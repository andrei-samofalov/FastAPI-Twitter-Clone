from datetime import datetime

from sqlalchemy import ForeignKey, String, func, Table, Column, Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    __abstract__ = True
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)


follow = Table(
    "follows",
    Base.metadata,
    Column("follower", Integer, ForeignKey("users.id"), primary_key=True),
    Column("followee", Integer, ForeignKey("users.id"), primary_key=True),
)


class User(Base):
    __tablename__ = "users"

    name: Mapped[str]
    followers: Mapped['User'] = relationship(
        secondary='follows',
        primaryjoin=id == follow.c.follower,
        secondaryjoin=id == follow.c.followee,
        backref="followee",
    )
    following: Mapped['User'] = relationship(
        secondary='follows',
        primaryjoin=id == follow.c.followee,
        secondaryjoin=id == follow.c.follower,
        backref="follower",
    )


class Tweet(Base):
    __tablename__ = 'tweets'

    tweet_data: Mapped[str]
    likes: Mapped[int]
    user_id: Mapped[int] = relationship(ForeignKey('users.id'))

    tweet_media_ids: Mapped[list['TweetMedia']] = relationship()


class TweetMedia(Base):
    __tablename__ = 'media'

    url: Mapped[str]
    tweet_id: Mapped[int] = mapped_column(ForeignKey('tweets.id'))
