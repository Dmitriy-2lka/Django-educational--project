from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

class Product(models.Model):
    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")


    name = models.CharField(max_length=15)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(default=0, max_digits=10, decimal_places=2, validators=[
            MinValueValidator(0),])
    discount = models.PositiveSmallIntegerField(default=0,validators=[MaxValueValidator(100),])
    creation_date = models.DateTimeField(auto_now_add = True)
    archived = models.BooleanField(default=False)
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='products',
    )

    def __str__(self):
        return f'Product {self.pk} - {self.name!r}'

    def get_absolute_url(self):
        return reverse('shopapp:products_details', kwargs={'pk': self.pk})

class Order(models.Model):

    class Meta:
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")

    delivery_address = models.TextField()
    promo = models.CharField(max_length=15, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    products = models.ManyToManyField(Product, related_name='orders')

    def __str__(self):
        return f'Order for user {self.user.first_name or self.user.username!r}'