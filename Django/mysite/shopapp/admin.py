from io import TextIOWrapper
from csv import DictReader

from django.contrib import admin
from django.db import transaction
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.urls import path
from django.contrib.auth.models import User

from .models import Product, Order
from .forms import CSVImportForm

class OrderInLine(admin.TabularInline):
    model = Product.orders.through

@admin.action(description='Archive product')
def mark_archived(modeladmin: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet):
    queryset.update(archivaed=True)

@admin.action(description='Unarchive product')
def mark_unarchived(modeladmin: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet):
    queryset.update(archivaed=False)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = 'pk', 'name', 'description', 'price', 'discount', 'archived'
    list_display_links = 'pk', 'name'
    search_fields = 'name', 'price', 'pk'
    inlines = [
        OrderInLine,
    ]
    fieldsets  = [
        (None, {'fields':
                    ('name', 'description')}),
        ('Price information', {'fields':
                    ('price', 'discount')}),
        ('Archived', {'fields':('archived',),
                    'classes': ('collapse',)})
    ]

    actions = [mark_archived, mark_unarchived]


class ProductInLine(admin.StackedInline):
    model = Order.products.through


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = 'pk', 'delivery_address', 'created_at', 'user'
    list_display_links = 'pk', 'delivery_address'
    search_fields = 'delivery_address', 'pk'
    inlines = [
        ProductInLine,
    ]
    change_list_template = 'shopapp/orders_changelist.html'

    def get_queryset(self, request):

        return Order.objects.select_related('user').prefetch_related('products')


    def import_csv(self, request: HttpRequest) -> HttpResponse:
        if request.method == "GET":
            form = CSVImportForm()
            context = {
                'form': form,
            }
            return render(request, 'admin/csv_form.html', context)

        form = CSVImportForm(request.POST, request.FILES)
        if not form.is_valid():
            context = {
                'form': form,
            }
            return render(request, 'admin/csv_form.html', context, status=400)

        csv_file = TextIOWrapper(
            form.files['csv_file'].file,
            encoding=request.encoding,
        )
        reader = DictReader(csv_file)


        with transaction.atomic():
            for order in reader:

                user_id = order.get('user')
                if user_id:
                    try:
                        user = User.objects.get(id=int(user_id))
                    except (User.DoesNotExist, ValueError):
                        user = request.user
                else:
                    user = request.user

                new_order = Order.objects.create(
                    delivery_address=order.get('delivery_address'),
                    promo=order.get('promo'),
                    user=user,
                )

                products_str = order.get('products')
                products_ids = [int(id) for id in products_str.split(',')]
                new_order.products.set(products_ids)

        self.message_user(request, "DATA from CSV wa imported")
        return redirect('..')

    def get_urls(self):
        urls = super().get_urls()
        new_urls = [
            path(
                'import-orders-csv/',
                self.import_csv,
                name='import-orders-csv'
            )
        ]
        return new_urls + urls