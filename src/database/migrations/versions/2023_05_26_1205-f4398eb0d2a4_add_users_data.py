"""add users data

Revision ID: f4398eb0d2a4
Revises: e7e342ea53f6
Create Date: 2023-05-26 12:05:08.066533

"""
from datetime import datetime

from alembic import op
from sqlalchemy import Integer, String, column, table, DateTime

# revision identifiers, used by Alembic.
revision = "f4398eb0d2a4"
down_revision = "e7e342ea53f6"
branch_labels = None
depends_on = None


def upgrade() -> None:

    users_table = table("users", column("name", String), column("api_key", String))

    op.bulk_insert(
        users_table,
        [
            {"name": "Mr. Fortran", "api_key": "test"},
            {"name": "Mrs. Delphi", "api_key": "admin"},
        ],
    )

    users_to_users_table = table(
        "user_follows", column("followers_id", Integer), column("following_id", Integer)
    )

    op.bulk_insert(
        users_to_users_table,
        [
            {"followers_id": 1, "following_id": 2},
            {"followers_id": 2, "following_id": 1},
        ],
    )

    tweets = table(
        "tweets", column("content", String), column("user_id", Integer),
        column("created_at", DateTime)
    )

    dt_format = "%Y-%m-%d %H:%M:%S.%f"

    op.bulk_insert(
        tweets,
        [
            {
                "content": "hello!",
                "user_id": 1,
                "created_at": datetime.strptime("2023-05-26 12:48:36.732685", dt_format)
            },
            {
                "content": "hello!",
                "user_id": 2,
                "created_at": datetime.strptime("2023-05-26 12:48:48.072168", dt_format)
            },
            {
                "content": "look at this beautiful forest!!",
                "user_id": 1,
                "created_at": datetime.strptime("2023-05-26 14:30:11.554886", dt_format)
            },
        ],
    )

    medias = table(
        "tweet_media", column("url", String), column("tweet_id", Integer)
    )

    op.bulk_insert(
        medias,
        [
            {"url": "/images/forest.webp", "tweet_id": 3},
        ],
    )

    likes = table(
        "tweet_likes", column("tweet_id", Integer), column("user_id", Integer)
    )

    op.bulk_insert(
        likes,
        [
            {"tweet_id": 1, "user_id": 2},
            {"tweet_id": 2, "user_id": 1},
            {"tweet_id": 3, "user_id": 2},
        ],
    )


def downgrade() -> None:
    pass
