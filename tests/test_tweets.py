import pytest
from loguru import logger


@pytest.mark.tweets
class TestTweets:
    """Test everything around tweets."""

    @pytest.fixture(autouse=True, scope='class')
    async def setup(self, async_session, user):
        """Setup test: adding mock user to database."""
        async with async_session.begin():
            async_session.add(user)

    async def test_add_tweet(self, tweet, async_client, async_session):
        """Test tweet can be added."""
        response = await async_client.post(
            '/api/tweets/',
            content=tweet.json(),
            headers={"api-key": "test"}
        )

        assert response.status_code == 201

    async def test_anonymous_user_cant_add_tweet(
            self, tweet, async_client, async_session
    ):
        """Test tweet can be added."""
        response = await async_client.post(
            '/api/tweets/',
            content=tweet.json(),
            headers={"api-key": "this api-key doesn't exist in database"}
        )

        assert response.status_code == 201

