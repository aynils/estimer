from django.conf import settings
from django.urls import path
from django.views.decorators.cache import cache_page

from src.dvf.data.cities import get_data_for_code_commune
from src.dvf.views import city

# urlpatterns = [path("<str:slug>", cache_page(settings.CACHE_TTL_ONE_DAY)(city), name="city")]
urlpatterns = [
    path("<str:slug>", city, name="city"),
    path("data/", get_data_for_code_commune, name="get_data_for_code_commune"),
]
