import pytest
from loguru import logger

from utils.service import Dal


@pytest.mark.tweets
class TestUsers:
    """Test everything around tweets."""

    @pytest.fixture(autouse=True, scope='class')
    async def setup(self, async_session, user_1):
        """Setup test: adding mock user to database."""
        async with async_session.begin():
            async_session.add(user_1)

    async def test_get_current_user(self, async_session, user_1):
        """Test func get_current_user."""
        curr_user = await Dal(async_session).get_current_user("test")
        assert curr_user.api_key == 'test'
        assert curr_user.id == 1
        assert curr_user.name == 'test'

    async def test_api_endpoint_user_by_id(
            self, async_session, async_client, user_1_expected
    ):
        """Test api/users/{idx}."""

        response = await async_client.get('/api/users/1')

        assert response.status_code == 200
        assert response.json() == user_1_expected

    async def test_api_endpoint_current_user(
            self, async_session, async_client, user_1_expected
    ):
        """Test api/users/me."""

        response = await async_client.get(
            '/api/users/me', headers={"api-key": "test"}
        )

        assert response.status_code == 200
        assert response.json() == user_1_expected
