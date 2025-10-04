from django.core.management import BaseCommand

from ...models import Product

class Command(BaseCommand):
    """
    Create products
    """

    def handle(self, *args, **options):
        self.stdout.write('Start create products')


        products = [
            {'name': 'apple', 'description': 'red and green apple', 'price': 6},
            {'name': 'banana', 'description': 'from Bolivia', 'price': 8},
            {'name': 'orange', 'description': 'just orange', 'price': 10},
            {'name': 'mango', 'price': 22},
        ]

        for product_data in products:
            product, created = Product.objects.get_or_create(name=product_data['name'], defaults=product_data)

            self.stdout.write(f'Created product {product.name}')

        self.stdout.write(self.style.SUCCESS('All products created'))



