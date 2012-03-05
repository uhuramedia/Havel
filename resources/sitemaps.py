from django.contrib.sitemaps import Sitemap
from resources.models import Resource
from django.utils import translation

class ResourceSitemap(Sitemap):

    def items(self):
        return Resource.objects.filter(noindex=False, is_published=True,
                                       language=translation.get_language())

    def lastmod(self, obj):
        return obj.modified
