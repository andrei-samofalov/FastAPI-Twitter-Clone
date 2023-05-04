from fastapi import FastAPI
from .tweets import router as tweets
from .users import router as users
# from .media import router as media


def create_app() -> FastAPI:
    app = FastAPI(
        debug=True,
        title='Twitter clone',

    )
    app.include_router(tweets)
    app.include_router(users)
    # app.include_router(media)

    return app

