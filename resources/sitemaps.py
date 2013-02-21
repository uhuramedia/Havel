from django.contrib.sitemaps import Sitemap
from resources.models import Resource, Page
from django.utils import translation

class ResourceSitemap(Sitemap):

    def items(self):
        return Page.objects.filter(noindex=False, is_published=True,
                                   language=translation.get_language())

    def lastmod(self, obj):
        return obj.modified
