from django import forms
from .models import Order, OrderItem, Supplier
from django.forms import inlineformset_factory, modelformset_factory

class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ['name', 'contact_person', 'email', 'phone', 'address', 'notes']



class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['supplier', 'expected_delivery', 'notes']
        
OrderItemFormSet = inlineformset_factory(
    Order,
    OrderItem,
    fields = ['variant', 'quantity', 'unit_price', 'notes'],
    extra=1,
    can_delete=False
)

DeliveryFormSet = modelformset_factory(
    OrderItem,
    fields=['delivered_quantity', 'notes'],
    extra=0
)