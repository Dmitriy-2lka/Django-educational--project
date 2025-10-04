from django.contrib.sitemaps import Sitemap

from .models import Product

class ShopSitemap(Sitemap):
    changefreq = 'never'
    priotity = 0.5

    def items(self):
        return Product.objects.filter(archived__isnull=False).order_by('-creation_date')

    def lastmod(self, obj: Product):
        return obj.creation_date