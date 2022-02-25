from .base import *

DEBUG = True

CACHES = {"default": {"BACKEND": "django.core.cache.backends.dummy.DummyCache"}}

INSTALLED_APPS += ["django_browser_reload"]

MIDDLEWARE += ["django_browser_reload.middleware.BrowserReloadMiddleware"]
