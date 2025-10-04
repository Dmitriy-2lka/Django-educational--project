from django.contrib.auth.models import User, Permission
from django.urls import reverse
from django.test import TestCase
from django.core.management import call_command

from shopapp.models import Order, Product


class OrderDetailViewTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.user = User.objects.create_user(username='test-user', password='test-password')
        view_order_perm = Permission.objects.get(codename='view_order')
        cls.user.user_permissions.add(view_order_perm)

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()

    def setUp(self):
        self.client.force_login(self.user)
        self.delivery_address = 'ul Test, d 88'
        self.promocode = 'test-promo'

        self.product = Product.objects.create(name='Test Product', price=100, created_by=self.user)

        self.order = Order.objects.create(
            user=self.user,
            delivery_address=self.delivery_address,
            promo=self.promocode,
        )
        self.order.products.set([self.product])

    def tearDown(self):
        self.order.delete()
        self.product.delete()


    def test_order_details(self):
        response = self.client.get(reverse(viewname='shopapp:order_details', kwargs={'pk': self.order.pk}))
        self.assertContains(response, self.delivery_address)
        self.assertContains(response, self.promocode)
        self.assertEqual(response.context['order'].pk, self.order.pk)


class OrdersExportTestCase(TestCase):

    fixtures = [
        'orders-fixture.json',
        'products-fixture.json',
        'users-fixture.json',
        'auth-group-fixture.json'
    ]

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.user = User.objects.create_user(username='test-user_staff', password='test-password')
        cls.user.is_staff=True
        cls.user.save()

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()

    def setUp(self):
        self.client.force_login(self.user)

    def test_get_orders_json(self):
        response = self.client.get(reverse(viewname='shopapp:orders_json'))
        self.assertEqual(response.status_code, 200)
        orders = Order.objects.order_by('pk').all()
        test_orders_data = [
            {
                'pk': order.pk,
                'delivery_address': order.delivery_address,
                'promo': order.promo,
                'user': order.user.pk,
                'products': [product.pk for product in order.products.all()],
            }
            for order in orders
        ]

        orders_data = response.json()

        print("\ntest_orders_data:", test_orders_data)
        print("orders_data:", orders_data['orders'])

        self.assertEqual(orders_data['orders'], test_orders_data)