from django.contrib.sitemaps.views import sitemap
from django.urls import path

from services.seo.sitemap import SpecialtySitemap, NewsSitemap
from services.seo.robots import robots_txt

sitemaps = {
    'news': NewsSitemap,
    'specialty': SpecialtySitemap,
}

urlpatterns = [
    path('sitemap.xml/', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path("robots.txt/", robots_txt),
]