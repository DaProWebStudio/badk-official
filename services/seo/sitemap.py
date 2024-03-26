from django.contrib.sitemaps import Sitemap

from apps.specialty.models import Specialty
from apps.news.models import News


class NewsSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.5

    def items(self):
        return News.active.all()

    def lastmod(self, obj):
        return obj.updated


class SpecialtySitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.9

    def items(self):
        return Specialty.active.all()

    def lastmod(self, obj):
        return obj.updated
