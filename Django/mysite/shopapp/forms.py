from django import forms

from shopapp.models import Product, Order


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = 'name', 'description', 'price', 'discount'

class OrderForm(forms.ModelForm):
    products = forms.ModelMultipleChoiceField(
        queryset=Product.objects.filter(archived=False),
        widget=forms.CheckboxSelectMultiple,
        required=True,
    )

    class Meta:
        model = Order
        fields = 'delivery_address', 'promo', 'products'


class CSVImportForm(forms.Form):
    csv_file = forms.FileField()
