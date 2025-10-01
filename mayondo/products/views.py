from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Product
from .forms import ProductForm, UnitForm, CategoryForm

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
def create_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product created successfully.')
            return redirect('product_list')
    else:
        form = ProductForm()
    context = { 
                'form': form,
                'title': 'Create Product',
                'product': None 
            }
    return render(request, 'products/create_product.html', context)

# Update product
@user_passes_test(is_manager, login_url='login_user')
def update_product(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product updated successfully.')
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)

    context = { 
               'form': form,
               'title': 'Update Product',
               'product': product, 
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






