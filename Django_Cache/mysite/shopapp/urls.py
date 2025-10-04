from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (shop_index,
                    ProductsListView, ProductsDetailView,
                    ProductCreateView, ProductUpdateView,
                    ProductDeleteView, OrdersListView,
                    OrdersDetailView, OrderCreateView,
                    OrderUpdateView, OrderDeleteView,
                    OrdersExportView, ProductListViewWithSerializer,
                    OrderListViewWithSerializer, LatestProductsFeed,
                    UserOrdersListView, UserOrdersExportView)

app_name = 'shopapp'

routers = DefaultRouter()
routers.register('products', ProductListViewWithSerializer)
routers.register('orders', OrderListViewWithSerializer)

urlpatterns = [
    path('', shop_index, name='shop_index'),
    path('products', ProductsListView.as_view(), name='products'),
    path('products/new', ProductCreateView.as_view(), name='create_product'),
    path('products/<int:pk>/', ProductsDetailView.as_view(), name='products_details'),
    path('products/<int:pk>/update', ProductUpdateView.as_view(), name='products_update'),
    path('products/<int:pk>/delete', ProductDeleteView.as_view(), name='product_delete'),

    path('orders', OrdersListView.as_view(), name='orders'),
    path('orders/new/', OrderCreateView.as_view(), name='create_order'),
    path('orders/<int:pk>/', OrdersDetailView.as_view(), name='order_details'),
    path('orders/<int:pk>/update', OrderUpdateView.as_view(), name='order_update'),
    path('orders/<int:pk>/delete', OrderDeleteView.as_view(), name='order_delete'),
    path('orders/export/', OrdersExportView.as_view(), name='orders_json'),
    path('orders/user/<int:user_id>', UserOrdersListView.as_view(), name='users_orders'),
    path('orders/user/<int:user_id>/export', UserOrdersExportView.as_view(), name='users_orders_export'),

    path('api/', include(routers.urls)),
    path('latest/feed/', LatestProductsFeed(), name='feed'),
]
