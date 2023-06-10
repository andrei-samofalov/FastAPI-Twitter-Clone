"""
Модуль содержит модели базы данных
"""
from datetime import datetime

from sqlalchemy import Column, ForeignKey, Integer, Table, func, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


user_to_user = Table(
    "user_follows",
    Base.metadata,
    Column("followers_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("following_id", Integer, ForeignKey("users.id"), primary_key=True),
)


class User(Base):
    """
    Модель юзера

    attrs:
        id - уникальный идентификатор юзера в БД, int
        username - имя юзера, str
        api_key - идентификатор на сервисе, str (хедер `api-key` запроса)

    relations:
        tweets - твиты, написанные юзером, o2m
        followers - юзеры, подписанные на текущего юзера, m2m
        following - юзеры, на которых подписан текущий юзер, m2m
    """

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True, index=True
    )
    name: Mapped[str] = mapped_column(nullable=False, unique=True, index=True)
    tweets: Mapped[list['Tweet']] = relationship(
        back_populates='author', cascade='all, delete-orphan', lazy='selectin'
    )
    api_key: Mapped[str] = mapped_column(unique=True, index=True)
    followers = relationship(
        "User",
        secondary=user_to_user,
        primaryjoin=id == user_to_user.c.following_id,
        secondaryjoin=id == user_to_user.c.followers_id,
        back_populates="following",
        lazy='selectin'
    )
    following = relationship(
        "User",
        secondary=user_to_user,
        primaryjoin=id == user_to_user.c.followers_id,
        secondaryjoin=id == user_to_user.c.following_id,
        back_populates="followers",
        lazy='selectin'
    )

    def __repr__(self):
        return f'User(id={self.id}, username={self.name})'


class Tweet(Base):
    """
    Модель твита

    attrs:
        id - уникальный идентификатор юзера в БД, int
        content - содержание твита, str
        user_id - id автора

    relations:
        likes - o2m связь с лайками
        tweet_media_ids - o2m связь с медиа
        author - o2o связь с автором твита

    """

    __tablename__ = 'tweets'

    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True, index=True
    )
    content: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    created_at: Mapped[datetime] = mapped_column(
        server_default=text('CURRENT_TIMESTAMP')
    )
    tweet_media_ids: Mapped[list['TweetMedia']] = relationship(lazy='selectin')

    likes: Mapped[list['TweetLike']] = relationship(
        back_populates='tweet', lazy='selectin', cascade="all, delete-orphan"
    )
    author: Mapped[User] = relationship(
        back_populates='tweets',
        lazy='selectin',
    )

    def __repr__(self):
        return f'Tweet(id={self.id}, user={self.author.name}'


class TweetMedia(Base):
    """
    Модель меда в твите

    attrs:
        id - уникальный идентификатор в БД, int
        url - адрес до файла на nginx?
        tweet_id - id твита, к которому этот медиа-файл прикреплен
    """

    __tablename__ = 'tweet_media'

    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True, index=True
    )
    url: Mapped[str]
    tweet_id: Mapped[int] = mapped_column(
        ForeignKey('tweets.id'), nullable=True
    )

    def __repr__(self):
        return f'TweetMedia(tweet_id={self.tweet_id}, url={self.url}'


class TweetLike(Base):
    """
    Модель лайка твита

    attrs:
        tweet_id - id твита
        user_id - id пользователя, поставившего лайк

    relations:
        tweet - o2o связь с твитом
        user - o2o связь с юзером, поставившем лайк
    """

    __tablename__ = 'tweet_likes'

    tweet_id: Mapped[int] = mapped_column(
        ForeignKey('tweets.id'), primary_key=True
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey('users.id'), primary_key=True
    )

    tweet: Mapped[Tweet] = relationship(
        back_populates='likes', lazy='selectin'
    )
    user: Mapped[User] = relationship(lazy='selectin')

    def __repr__(self):
        return f'TweetLike(tweet_id={self.tweet_id}'
