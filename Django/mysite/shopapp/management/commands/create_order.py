from django.contrib.auth.models import User
from django.core.management import BaseCommand

from random import choices

from ...models import Order, Product


class Command(BaseCommand):
    """
    Create order
    """

    def handle(self, *args, **options):
        self.stdout.write("Starting create order")

        users = [
            ('admin', 'st Pobbedy, 26'),
            ('notadmin', 'st Fialok, 15b, 2'),
        ]

        products = Product.objects.all()

        for user_data in users:

            user = User.objects.get(username=user_data[0])
            order, created = Order.objects.get_or_create(
                delivery_address=user_data[1],
                user=user,
            )

            for product in choices(products, k=2):
                order.products.add(product)

            order.save()

            self.stdout.write(f'Created order id - {order.id}')
