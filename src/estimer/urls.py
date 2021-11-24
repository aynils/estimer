"""estimer URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import path
from django.views.decorators.cache import cache_page

from dvf.views import city
from estimer.settings import CACHE_TTL_ONE_DAY
from estimer.sitemaps import CitySitemap
from estimer.views import home, mentions_legales

sitemaps = {"city": CitySitemap}

urlpatterns = [
    path("admin/", admin.site.urls),
    # path('account/', include('django.contrib.auth.urls')),
    path("commune/<str:slug>", cache_page(CACHE_TTL_ONE_DAY)(city), name="city"),
    path("mentions-legales", mentions_legales, name="mentions-legales"),
    path("", cache_page(CACHE_TTL_ONE_DAY)(home), name="home"),
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="django.contrib.sitemaps.views.sitemap"),
    # path("test/<str:code_iris>", get_mutations_by_iris, name="test"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
