from django import forms
from django.forms import inlineformset_factory
from .models import Product, ProductVariant, Unit, Category

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name", "category", "unit", "supplier", "description"]

class ProductVariantForm(forms.ModelForm):
    class Meta:
        model = ProductVariant
        fields = ["variant_name", "price", "stock_quantity", "is_active"]

ProductVariantFormSet = inlineformset_factory(
    Product,
    ProductVariant,
    form=ProductVariantForm,
    fields=["variant_name", "price", "stock_quantity", "is_active"],
    extra=1,
    can_delete=False
)

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name", "description"]

class UnitForm(forms.ModelForm):
    class Meta:
        model = Unit
        fields = ["name"]
