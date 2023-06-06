import pytest

from utils.service import Dal


@pytest.mark.users
class TestUsers:
    """Test everything around users."""

    @pytest.fixture(autouse=True, scope='class')
    async def setup(self, async_session, user_1, user_2):
        """Setup test: adding mock user to database."""
        async_session.add_all([user_1, user_2])
        await async_session.commit()
        yield
        await async_session.close()

    async def test_get_current_user(self, async_session, user_1):
        """Test func get_current_user."""
        curr_user = await Dal(async_session).get_current_user("test")
        assert curr_user.api_key == 'test'
        assert curr_user.id == 1
        assert curr_user.name == 'test'

    async def test_api_endpoint_user_by_id(
            self, async_client, user_1_expected
    ):
        """Test api/users/{idx}."""

        response = await async_client.get('/api/users/1')

        assert response.status_code == 200
        assert response.json() == user_1_expected

    async def test_api_endpoint_current_user(
            self, async_client, user_1_expected
    ):
        """Test api/users/me."""

        response = await async_client.get(
            '/api/users/me', headers={"api-key": "test"}
        )

        assert response.status_code == 200
        assert response.json() == user_1_expected

    async def test_user_can_follow_another_user(
            self, async_client, async_session, user_1, user_2
    ):
        response = await async_client.post(
            f'api/users/{user_2.id}/follow', headers={"api-key": user_1.api_key}
        )

        assert response.status_code == 200

        await async_session.refresh(user_1)
        await async_session.refresh(user_2)

        assert len(user_1.following) == 1
        assert user_2 in user_1.following
