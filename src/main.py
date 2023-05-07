from routers import create_app

import sentry_sdk


sentry_sdk.init(
    dsn="http://abaada4710cd43079dd757b96e3df3f3@localhost:9000/4",
    traces_sample_rate=1.0,
)

app = create_app()
