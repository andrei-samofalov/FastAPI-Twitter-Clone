from datetime import datetime

from sqlalchemy import ForeignKey, String, func, Table, Column, Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, backref


class Base(DeclarativeBase):
    pass


class UserToUser(Base):
    __tablename__ = 'user_follows'

    slave_id: Mapped[int] = mapped_column(
        ForeignKey('users.id'), primary_key=True
    )
    master_id: Mapped[int] = mapped_column(
        ForeignKey('users.id'), primary_key=True
    )

    slave: Mapped['User'] = relationship(
        back_populates='following',
        foreign_keys=[slave_id],
    )
    master: Mapped['User'] = relationship(
        back_populates='followers',
        foreign_keys=[master_id],
    )

    def __repr__(self):
        return f'{self.master} - {self.slave.info}'


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True, index=True
    )
    name: Mapped[str] = mapped_column(nullable=False, unique=True, index=True)
    tweets: Mapped[list['Tweet']] = relationship(
        back_populates='author', lazy='selectin', cascade='all, delete-orphan'
    )
    api_key: Mapped[str] = mapped_column(unique=True, index=True)
    followers: Mapped[list[UserToUser]] = relationship(
        back_populates="master",
        primaryjoin="User.id==UserToUser.master_id",
        lazy='joined',
    )
    following: Mapped[list[UserToUser]] = relationship(
        back_populates="slave",
        primaryjoin="User.id==UserToUser.slave_id",
        lazy='joined',
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
    author: Mapped[User] = relationship(
        back_populates='tweets', lazy='selectin'
    )

    def __repr__(self):
        return f'Tweet(id={self.id}, user={self.author.name}'


class TweetMedia(Base):
    __tablename__ = 'tweet_media'

    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True, index=True
    )
    url: Mapped[str]
    tweet_id: Mapped[int] = mapped_column(ForeignKey('tweets.id'))


class TweetLike(Base):
    __tablename__ = 'tweet_likes'

    tweet_id: Mapped[int] = mapped_column(
        ForeignKey('tweets.id'), primary_key=True
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey('users.id'), primary_key=True
    )

    tweet: Mapped[Tweet] = relationship()
    user: Mapped[User] = relationship()
