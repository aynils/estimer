from django.urls import path

from src.agencies.views import agency, get_cities_pricing

urlpatterns = [
    path("", agency, name="agence"),
    path("pricing/", get_cities_pricing, name="get_cities_pricing"),
]
