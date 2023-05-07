from datetime import datetime

from sqlalchemy import ForeignKey, String, func, Table, Column, Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


follows = Table(
    "follows",
    Base.metadata,
    Column("follower_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("following_id", Integer, ForeignKey("users.id"), primary_key=True),
)


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True, index=True
    )
    name: Mapped[str] = mapped_column(nullable=False, unique=True, index=True)
    tweets: Mapped[list['Tweet']] = relationship(
        back_populates='author', lazy='selectin', cascade='all, delete-orphan'
    )
    api_key: Mapped[str] = mapped_column()
    following = relationship(
        'User',
        secondary=follows,
        primaryjoin=id == follows.c.follower_id,
        secondaryjoin=id == follows.c.following_id,
        backref="followers",
        lazy='selectin',
    )

    def __repr__(self):
        return f'User(id={self.id}, name={self.name})'


class Tweet(Base):
    __tablename__ = 'tweets'

    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True, index=True
    )
    content: Mapped[str]
    likes: Mapped[list['TweetLike']] = relationship(
        back_populates='tweet', lazy='selectin'
    )
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))

    tweet_media_ids: Mapped[list['TweetMedia']] = relationship()
    author: Mapped[User] = relationship(back_populates='tweets', lazy='selectin')


class TweetMedia(Base):
    __tablename__ = 'media'

    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True, index=True
    )
    url: Mapped[str]
    tweet_id: Mapped[int] = mapped_column(ForeignKey('tweets.id'))


class TweetLike(Base):
    __tablename__ = 'tweetlikes'

    tweet_id: Mapped[int] = mapped_column(
        ForeignKey('tweets.id'), primary_key=True
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey('users.id'), primary_key=True
    )

    tweet: Mapped[Tweet] = relationship()
    user: Mapped[User] = relationship()
