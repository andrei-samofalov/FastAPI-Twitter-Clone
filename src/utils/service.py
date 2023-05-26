from fastapi import HTTPException, UploadFile
from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload
from starlette import status

from database.models import Tweet, TweetLike, TweetMedia, User
from schemas.tweet_schema import TweetIn
from utils.file_system import write_file


class Dal:
    """Data access layer."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_current_user(self, api_key: str) -> User:
        """Возвращает пользователя по api key."""
        stmt = (
            select(User)
            .filter_by(api_key=api_key)
            .options(
                selectinload(User.following), selectinload(User.followers)
            )
        )

        return await self._session.scalar(stmt)

    async def get_user_by_idx(self, idx: int):
        """Возвращает юзера по id."""
        stmt = (
            select(User)
            .filter_by(id=idx)
            .options(joinedload(User.following), joinedload(User.followers))
        )
        user = await self._session.scalar(stmt)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found.",
            )
        return user

    async def get_all_tweets(self, user: User):
        """
        Возвращает все твиты в порядке убывания даты создания
        читаемых пользователей + свои твиты для конкретного юзера.
        """

        # получаем все id читаемых пользователей и добавляем свой
        ids = [f.id for f in user.following] + [user.id]

        stmt = (
            select(Tweet)
            .where(Tweet.user_id.in_(ids))
            .options(
                selectinload(Tweet.author),
                selectinload(Tweet.likes),
                selectinload(Tweet.tweet_media_ids),
            )
            .order_by(desc(Tweet.created_at))
        )
        tweets = await self._session.scalars(stmt)

        return tweets.all()

    async def _get_like(self, tweet_id: int, user_id: int) -> TweetLike:
        """Возвращает лайк твита по id твита и пользователя."""
        stmt = select(TweetLike).where(
            TweetLike.user_id == user_id, TweetLike.tweet_id == tweet_id
        )

        return await self._session.scalar(stmt)

    async def _get_tweet(self, tweet_id) -> Tweet:
        """Возвращает твит по id."""
        stmt = select(Tweet).filter_by(id=tweet_id)

        return await self._session.scalar(stmt)

    async def add_tweet(self, tweet: TweetIn, user_id: int) -> Tweet:
        """
        Создает новый твит.
        Если получен список медиа, прикрепляет их к данному твиту.
        """

        new_tweet = Tweet(content=tweet.tweet_data, user_id=user_id)
        self._session.add(new_tweet)
        await self._session.flush()

        if ids := tweet.tweet_media_ids:
            await self._bind_media_to_tweet(ids, new_tweet.id)

        await self._session.commit()

        return new_tweet

    async def add_like_to_tweet(self, tweet_id: int, user_id: int) -> None:
        """Добавляет лайк твиту от конкретного юзера."""
        tweet = await self._get_tweet(tweet_id)

        if not await self._get_like(tweet_id=tweet_id, user_id=user_id):
            like = TweetLike(user_id=user_id, tweet_id=tweet.id)

            self._session.add(like)
            await self._session.commit()

    async def remove_like_from_tweet(
            self, tweet_id: int, user_id: int
    ) -> None:
        """Удаляет лайк с твита."""
        tweet = await self._get_tweet(tweet_id)

        like = await self._get_like(tweet_id=tweet.id, user_id=user_id)
        if like:
            await self._session.delete(like)
            await self._session.commit()

    async def delete_tweet(self, tweet_id: int, user_id: int):
        """
        Удаляет твит по id твита и пользователя.

        :raises HTTPException: Когда происходит попытка удаления чужого твита.
        """
        tweet = await self._get_tweet(tweet_id)
        if tweet.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access forbidden",
            )
        await self._session.delete(tweet)
        await self._session.commit()

    async def _bind_media_to_tweet(self, ids: list, tweet_id: int):
        """Связывает медиафайлы с твитом."""
        stmt = select(TweetMedia).filter(TweetMedia.id.in_(ids))

        medias = await self._session.scalars(stmt)
        for media in medias:
            if not media.tweet_id:
                media.tweet_id = tweet_id

        self._session.add_all(medias)

    async def upload_file(self, file: UploadFile):
        """Записывает в файл в память."""
        new_filename = await write_file(file)
        if new_filename:
            new_file = TweetMedia(url=new_filename)
            self._session.add(new_file)
            await self._session.commit()
            return new_file
