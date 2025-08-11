# store/forms.py
from django import forms
from .models import Product, ShippingAddress

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'image']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

class AddressForm(forms.ModelForm):
    class Meta:
        model = ShippingAddress
        fields = ['address_line_1', 'address_line_2', 'city', 'state', 'postal_code', 'country']
        labels = {
            'address_line_1': 'Address Line 1',
            'address_line_2': 'Address Line 2 (Optional)',
            'city': 'City / Town / Village',
            'state': 'State',
            'postal_code': 'Postal Code / PIN',
            'country': 'Country',
        }