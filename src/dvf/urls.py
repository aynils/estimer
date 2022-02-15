from django.conf import settings
from django.urls import path
from django.views.decorators.cache import cache_page

from src.dvf.views import city

urlpatterns = [path("<str:slug>", cache_page(settings.CACHE_TTL_ONE_DAY)(city), name="city")]
