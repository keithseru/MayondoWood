from django import forms
from .models import Sale, SaleItem, Customer
from django.forms import inlineformset_factory

class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ['customer', 'notes']

SaleItemFormSet = inlineformset_factory(
    Sale,
    SaleItem,
    fields=['product_variant', 'quantity', 'unit_price'],
    extra=2,
    can_delete=True
)

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'address']