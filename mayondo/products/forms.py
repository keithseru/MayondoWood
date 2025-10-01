from django import forms
from .models import Product, Unit, Category

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name", "category", "unit", "price", "description"]

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name", "description"]

class UnitForm(forms.ModelForm):
    class Meta:
        model = Unit
        fields = ["name"]
