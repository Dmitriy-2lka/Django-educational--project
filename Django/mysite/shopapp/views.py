from django.http import HttpRequest, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, reverse, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.core.cache import cache
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.contrib.syndication.views import Feed
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.models import User

from .mixins import OwnerRequiredMixin
from .models import Product, Order
from .serializers import ProductSerializer, OrderSerializer


def shop_index(request: HttpRequest):
    context = {
        'list_index': ['products', 'orders'],
    }
    return render(request, 'shopapp/index.html', context=context)


class ProductsListView(ListView):
    template_name = 'shopapp/products.html'
    model = Product
    context_object_name = 'list_products'


class ProductsDetailView(DetailView):
    template_name = 'shopapp/products_details.html'
    model = Product
    context_object_name = 'product'


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    fields = 'name', 'price', 'description', 'discount'
    success_url = reverse_lazy('shopapp:products')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class ProductUpdateView(PermissionRequiredMixin, OwnerRequiredMixin, UpdateView):
    permission_required = 'shopapp.change_product'
    model = Product
    fields = 'name', 'price', 'description', 'discount'
    template_name_suffix = '_update'

    def get_success_url(self):
        return reverse(
            'shopapp:products_details',
            kwargs={'pk': self.object.pk},
        )


class ProductDeleteView(PermissionRequiredMixin, OwnerRequiredMixin, DeleteView):
    permission_required = 'shopapp.delete_product'
    model = Product
    success_url = reverse_lazy('shopapp:products')

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.archived = True
        self.object.save()
        return HttpResponseRedirect(success_url)


class OrdersListView(ListView):
    template_name = 'shopapp/orders.html'
    model = Order
    context_object_name = 'orders'


class OrdersDetailView(PermissionRequiredMixin, DetailView):
    queryset = (
        Order.objects
        .select_related('user')
        .prefetch_related('products')
    )

    permission_required = 'shopapp.view_order'
    template_name = 'shopapp/order_details.html'
    model = Order
    context_object_name = 'order'


class OrderCreateView(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    permission_required = 'shopapp.add_order'
    model = Order
    fields = 'delivery_address', 'promo', 'products'
    success_url = reverse_lazy('shopapp:orders')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class OrderUpdateView(UpdateView):
    model = Order
    fields = 'delivery_address', 'promo', 'products'
    template_name_suffix = '_update'

    def get_success_url(self):
        return reverse(
            'shopapp:order_details',
            kwargs={'pk': self.object.pk},
        )


class OrderDeleteView(DeleteView):
    model = Order
    success_url = reverse_lazy('shopapp:orders')


class OrdersExportView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        return (self.request.user.is_staff == True)

    def get(self, request: HttpRequest) -> JsonResponse:
        orders = Order.objects.order_by('pk').all()
        orders_data = [
            {
                'pk': order.pk,
                'delivery_address': order.delivery_address,
                'promo': order.promo,
                'user': order.user.pk,
                'products': [product.pk for product in order.products.all()],
            }
            for order in orders
        ]

        return JsonResponse({'orders': orders_data})


class ProductListViewWithSerializer(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [
        SearchFilter,
        OrderingFilter
    ]
    search_fields = [
        'name',
        'description',
        'price',
    ]
    ordering_fileds = [
        'pk',
        'name',
        'description',
        'price',
    ]


class OrderListViewWithSerializer(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filter_backends = [
        DjangoFilterBackend,
        OrderingFilter
    ]
    filterset_fields = [
        'delivery_address',
        'user',
        'products',
    ]
    ordering_fields = [
        'pk',
        'created_at',
        'user',
    ]


class LatestProductsFeed(Feed):
    title = 'Latest Products'
    description = 'Update products list in shop'
    link = reverse_lazy('shopapp:products')

    def items(self):
        return Product.objects.filter(archived__isnull=False).order_by('-creation_date')[:5]

    def item_title(self, item: Product):
        return item.name

    def item_description(self, item: Product):
        return item.description[:30]


class UserOrdersListView(LoginRequiredMixin, ListView):
    template_name = 'shopapp/users_orders.html'
    context_object_name = 'orders'
    model = Order

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        self.owner = get_object_or_404(User, pk=user_id)
        return (
            Order.objects
            .select_related('user')
            .prefetch_related('products')
            .filter(user=self.owner)
            .order_by('pk')
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['owner'] = self.owner
        return context


class UserOrdersExportView(LoginRequiredMixin, View):

    def get(self, request: HttpRequest, user_id) -> JsonResponse:

        cache_key = f'orders_data_{user_id}'

        orders_data = cache.get(cache_key)

        if orders_data is None:
            user = get_object_or_404(User, pk=user_id)

            orders = (
                Order.objects
                .select_related('user')
                .prefetch_related('products')
                .filter(user=user)
                .order_by('pk')
            )

            orders_data = OrderSerializer(orders, many=True)

            cache.set(cache_key, orders_data, 180)

        return JsonResponse({'orders': orders_data.data})
