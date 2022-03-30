from .base import *

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

DEBUG = False

sentry_sdk.init(
    dsn="https://64223d840fca4d42a7b23457ffa6c23e@o889756.ingest.sentry.io/5838890",
    integrations=[DjangoIntegration()],
    environment=os.getenv("DJANGO_ENV"),
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=0.01,
    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=False,
)


SESSION_CACHE_ALIAS = "production"

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": os.getenv("REDIS_URL"),
        "OPTIONS": {"CLIENT_CLASS": "django_redis.client.DefaultClient"},
        "KEY_PREFIX": "estimer_v2.1.8",
    }
}
