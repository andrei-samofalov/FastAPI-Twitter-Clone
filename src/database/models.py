"""
Модуль содержит модели базы данных
"""

from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class UserToUser(Base):
    """
    Таблица ассоциации юзеров для подписки

    slave - тот, кто подписывается
    master - тот, на кого подписываются
    """
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
    """
    Модель юзера

    attrs:
        id - уникальный идентификатор юзера в БД, int
        name - имя юзера, str
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
    """
    Модель твита

    attrs:
        id - уникальный идентификатор юзера в БД, int
        content - содержание твита, str
        user_id - id автора

    relations:
        likes - o2m связь с лайками
        tweet_media_ids - o2m связь с медиа # TODO переделать
        author - o2o связь с автором твита

    """
    __tablename__ = 'tweets'

    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True, index=True
    )
    content: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))

    likes: Mapped[list['TweetLike']] = relationship(
        back_populates='tweet', lazy='selectin'
    )
    tweet_media_ids: Mapped[list['TweetMedia']] = relationship()
    author: Mapped[User] = relationship(
        back_populates='tweets', lazy='selectin'
    )

    def __repr__(self):
        return f'Tweet(id={self.id}, user={self.author.name}'


class TweetMedia(Base):
    """
    Модель меда в твите

    # TODO
    Пока не ясно, как это реализовывать.
    По идее, должен файл сохраняться на сервере nginx в отдельную папку
    Подумать над валидацией (может быть, есть встроенная?)
    нужно ли прописать relations?

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
    tweet_id: Mapped[int] = mapped_column(ForeignKey('tweets.id'))

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

    tweet: Mapped[Tweet] = relationship(back_populates='likes', lazy='selectin')
    user: Mapped[User] = relationship()

    def __repr__(self):
        return f'TweetLike(tweet_id={self.tweet_id}'
