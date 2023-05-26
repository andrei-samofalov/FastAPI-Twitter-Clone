import pytest
from loguru import logger
from sqlalchemy import select

from database import models


@pytest.mark.tweets
class TestTweets:
    """Test everything around tweets."""

    @pytest.fixture(autouse=True, scope='class')
    async def setup(self, async_session, user):
        """Setup test: adding mock user to database."""
        async with async_session.begin():
            async_session.add(user)
        logger.debug('Test user added to test database')

    async def test_add_tweet(self, tweet, async_client, async_session):
        """Test tweet can be added by registered user (api-key)."""

        response = await async_client.post(
            '/api/tweets/',
            content=tweet,
            headers={"api-key": "test"}
        )

        assert response.status_code == 201

        new_tweet_id = response.json().get('id')

        # записываем новое значение количества твитов в бд
        async with async_session.begin():
            q = select(models.Tweet)
            result = await async_session.scalars(q)
            new_tweets = result.all()

            new_tweets_amount = len(new_tweets)
            new_tweet = new_tweets[0]

        assert new_tweet.id == new_tweet_id
        assert new_tweets_amount == 1

        assert response.json() == {"result": True, "id": 1}

    async def test_anonymous_user_cannot_add_tweet(
            self, tweet, async_client, async_session
    ):
        """Test tweet cannot be added by user with unregistered api-key."""
        response = await async_client.post(
            '/api/tweets/',
            content=tweet,
            headers={"api-key": "this api-key doesn't exist in database"}
        )

        # ожидаем, что при незарегистрированном apy-key вызывается HTTPException
        # который вернет {"detail": "not found"} и код 404
        assert response.status_code == 404
        assert response.json() == {'detail': 'not found'}

