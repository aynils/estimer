from django.urls import path

from src.agencies.views import agency

urlpatterns = [
    path("", agency, name="agence"),
]
