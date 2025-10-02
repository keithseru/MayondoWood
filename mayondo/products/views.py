from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Product
from .forms import ProductForm, UnitForm, CategoryForm, ProductVariantFormSet

# Create your views here.

def is_manager(user):
    return user.is_authenticated and user.role == 'MANAGER'

# Viewable by all roles
@login_required
def product_list(request):
    products = Product.objects.select_related('category', 'unit').all()
    context = {'products': products}
    return render(request, 'products/product_list.html', context)

#Product Item Detail
@login_required
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, "products/product_detail.html", {
        "product": product,
        "title": "Product Details"
    })

# Manager only views
# Create product
@user_passes_test(is_manager, login_url='login_user')
@login_required
def create_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        formset = ProductVariantFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            product = form.save()
            formset.instance = product
            formset.save()
            messages.success(request, 'Product and variants created successfully.')
            return redirect('product_list')
    else:
        form = ProductForm()
        formset = ProductVariantFormSet()

    context = {
        'form': form,
        'formset': formset,
        'title': 'Create Product',
        'product': None
    }
    return render(request, 'products/create_product.html', context)

# Update product
@user_passes_test(is_manager, login_url='login_user')
@login_required
def update_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    formset = ProductVariantFormSet(request.POST or None, instance=product)

    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            messages.success(request, 'Product and variants updated successfully.')
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)

    context = {
        'form': form,
        'formset': formset,
        'title': 'Update Product',
        'product': product
    }
    return render(request, 'products/create_product.html', context)

# Create Category
@user_passes_test(is_manager, login_url='login_user')
def create_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category created successfully.')
            return redirect('product_list')
    else:
        form = CategoryForm()
    context = { 
               'form' : form,
               'title' : "Category",
            }
    return render(request, 'products/create_category.html', context)

#Create Unit
@user_passes_test(is_manager, login_url='login_user')
def create_unit(request):
    if request.method == 'POST':
        form = UnitForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Unit created successfully.')
            return redirect('unit_list')
    else:
        form = UnitForm()
    context = { 
               'form' : form,
               'title' : "Unit",
            }
    return render(request, 'products/create_category.html', context)

@user_passes_test(is_manager, login_url="login_user")
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == "POST":
        product.delete()
        messages.success(request, "Product deleted successfully.")
        return redirect("product_list")

    return render(request, "products/delete_product.html", {
        "product": product,
        "title": "Delete Product"
    })






