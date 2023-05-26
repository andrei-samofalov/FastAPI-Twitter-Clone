from fastapi import FastAPI

from routers.media import router as media
from routers.tweets import router as tweets
from routers.users import router as users


def create_app() -> FastAPI:
    """
    Initialize a FastAPI application,
    connect the necessary routers, dependencies, and handlers.
    :rtype: FastAPI
    """
    app = FastAPI(
        debug=True,
        title='Twitter clone',
    )
    app.include_router(
        tweets,
        prefix="/api",
    )
    app.include_router(
        users,
        prefix="/api",
    )
    app.include_router(
        media,
        prefix="/api",
    )

    return app
