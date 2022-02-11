from django.urls import path

from src.iris.views import get_data_for_iris

urlpatterns = [path("data/", get_data_for_iris, name="get_data_for_iris")]
