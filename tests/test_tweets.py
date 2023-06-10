import pytest
from sqlalchemy import select

from database import models


@pytest.mark.tweets
class TestTweets:
    """Test everything around tweets."""

    @pytest.fixture(autouse=True, scope='class')
    async def setup(self, async_session, user_1, tweetDB_us1):
        """Setup test: adding mock user to database."""
        async with async_session.begin():
            async_session.add(user_1)
            async_session.add(tweetDB_us1)
        yield
        await async_session.delete(user_1)

    async def test_add_tweet(self, tweet, async_client, async_session):
        """Test tweet can be added by registered user (api-key)."""

        response = await async_client.post(
            '/api/tweets/',
            content=tweet,
            headers={"api-key": "test"}
        )

        assert response.status_code == 201

        new_tweet_id = response.json().get('tweet_id')

        # записываем новое значение количества твитов в бд
        async with async_session.begin():
            q = select(models.Tweet)
            result = await async_session.scalars(q)
            new_tweets = result.all()

            new_tweets_amount = len(new_tweets)
            new_tweet = new_tweets[1]

        assert new_tweet.id == new_tweet_id
        assert new_tweets_amount == 2

        assert response.json() == {"result": True, "tweet_id": 2}

    async def test_add_like_to_tweet(
            self, tweetDB_us1, async_client, async_session, user_1
    ):
        """Test like can be added to tweet."""
        assert tweetDB_us1.author == user_1

        response = await async_client.post(
            f'api/tweets/{tweetDB_us1.id}/likes',
            headers={"api-key": f"{user_1.api_key}"}
        )
        assert response.status_code == 201
        await async_session.refresh(tweetDB_us1)

        assert len(tweetDB_us1.likes) == 1

    async def test_delete_like(
            self, tweetDB_us1, async_client, async_session, user_1
    ):
        """Test tweet like can be deleted."""
        assert tweetDB_us1.author == user_1

        response = await async_client.delete(
            f'api/tweets/{tweetDB_us1.id}/likes',
            headers={"api-key": f"{user_1.api_key}"}
        )

        assert response.status_code == 200
        await async_session.refresh(tweetDB_us1)
        assert len(tweetDB_us1.likes) == 0

    async def test_delete_tweet_by_another_user(
            self, tweetDB_us1, async_client, async_session, user_1, user_2
    ):
        """Test tweet can be deleted by owner."""
        async_session.add(user_2)
        await async_session.commit()

        response = await async_client.delete(
            f'api/tweets/{tweetDB_us1.id}',
            headers={"api-key": f"{user_2.api_key}"}
        )

        assert response.status_code == 403
        await async_session.refresh(user_1)

        assert len(user_1.tweets) == 2

        await async_session.delete(user_2)

    async def test_delete_tweet_by_owner(
            self, tweetDB_us1, async_client, async_session, user_1
    ):
        """Test tweet can be deleted by owner."""

        response = await async_client.delete(
            f'api/tweets/{tweetDB_us1.id}',
            headers={"api-key": f"{user_1.api_key}"}
        )

        assert response.status_code == 200
        await async_session.refresh(user_1)

        assert len(user_1.tweets) == 1

    async def test_anonymous_user_cannot_add_tweet(
            self, tweet, async_client
    ):
        """Test tweet cannot be added by user with unregistered api-key."""
        response = await async_client.post(
            '/api/tweets/',
            content=tweet,
            headers={"api-key": "this api-key doesn't exist in database"}
        )

        # ожидаем, что при незарегистрированном apy-key вызывается HTTPException
        # который вернет "Could not validate credentials" и код 401
        assert response.status_code == 401
        assert response.json() == {'detail': "Could not validate credentials"}
