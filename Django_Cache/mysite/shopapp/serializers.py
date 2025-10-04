from .models import Product, Order
from rest_framework.serializers import ModelSerializer


class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = 'pk', 'name', 'description', 'price', 'discount', 'archived', 'creation_date'

class OrderSerializer(ModelSerializer):
    class Meta:
        model = Order
        fields = 'pk', 'delivery_address', 'created_at', 'user', 'products'