import sentry_sdk

from routers import create_app
from utils.settings import USE_SENTRY, get_settings

if USE_SENTRY:
    s = get_settings()
    sentry_sdk.init(
        dsn=s.sentry_dsn,
        traces_sample_rate=1.0,
    )

app = create_app()
