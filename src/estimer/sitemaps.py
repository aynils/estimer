import datetime

from django.contrib.sitemaps import Sitemap
from dvf.models import Commune


class CitySitemap(Sitemap):
    changefreq = "yearly"
    priority = 0.5

    def items(self):
        return Commune.objects.all()

    def lastmod(self, obj):
        return datetime.datetime.now()
