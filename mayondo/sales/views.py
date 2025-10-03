from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Sale, Customer
from .forms import SaleForm, SaleItemFormSet, CustomerForm

def is_manager(user):
    return user.is_authenticated and user.role == 'MANAGER'

def is_sales_or_manager(user):
    return user.is_authenticated and user.role in ['SALES', 'MANAGER']

# Sale Views
@login_required
@user_passes_test(is_sales_or_manager, login_url='login_user')
def sale_list(request):
    sales = Sale.objects.select_related('customer', 'created_by').prefetch_related('items__product_variant')
    return render(request, 'sales/sale_list.html', {
        'sales': sales,
        'title': 'Sales'
    })

@login_required
@user_passes_test(is_sales_or_manager, login_url='login_user')
def create_sale(request):
    if request.method == 'POST':
        form = SaleForm(request.POST)
        formset = SaleItemFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            sale = form.save(commit=False)
            sale.created_by = request.user.employee  # assuming request.user is linked to Employee
            sale.save()
            formset.instance = sale
            formset.save()
            messages.success(request, "Sale recorded successfully.")
            return redirect('sale_detail', pk=sale.pk)
    else:
        form = SaleForm()
        formset = SaleItemFormSet()

    return render(request, 'sales/create_sale.html', {
        'form': form,
        'formset': formset,
        'title': 'Record Sale'
    })

@login_required
@user_passes_test(is_sales_or_manager, login_url='login_user')
def sale_detail(request, pk):
    sale = get_object_or_404(Sale.objects.prefetch_related('items__product_variant'), pk=pk)
    return render(request, 'sales/sale_detail.html', {
        'sale': sale,
        'title': f"Sale #{sale.id} Details"
    })
    
@login_required
@user_passes_test(is_sales_or_manager, login_url='login_user')
def update_sale(request, pk):
    sale = get_object_or_404(Sale, pk=pk)
    form = SaleForm(request.POST or None, instance=sale)
    formset = SaleItemFormSet(request.POST or None, instance=sale)

    if request.method == 'POST':
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            messages.success(request, "Sale updated successfully.")
            return redirect('sale_detail', pk=sale.pk)

    return render(request, 'sales/update_sale.html', {
        'form': form,
        'formset': formset,
        'title': f"Update Sale #{sale.id}"
    })

@login_required
@user_passes_test(is_manager, login_url='login_user')
def delete_sale(request, pk):
    sale = get_object_or_404(Sale, pk=pk)
    if request.method == 'POST':
        sale.delete()
        messages.success(request, "Sale deleted.")
        return redirect('sale_list')
    return render(request, 'sales/delete_sale.html', {
        'sale': sale,
        'title': f"Delete Sale #{sale.id}"
    })
    
# Customer Management Views
@login_required
@user_passes_test(is_sales_or_manager, login_url='login_user')
def create_customer(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Customer added.")
            return redirect('sale_list')
    else:
        form = CustomerForm()
    return render(request, 'sales/create_customer.html', {
        'form': form,
        'title': 'Add Customer'
    })
    
@login_required
@user_passes_test(is_sales_or_manager, login_url='login_user')
def customer_list(request):
    customers = Customer.objects.all().order_by('last_name', 'first_name')
    return render(request, 'sales/customer_list.html', {
        'customers': customers,
        'title': 'Customer List'
    })
    
@login_required
@user_passes_test(is_sales_or_manager, login_url='login_user')
def update_customer(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            messages.success(request, "Customer updated successfully.")
            return redirect('sale_list')
    else:
        form = CustomerForm(instance=customer)
    return render(request, 'sales/update_customer.html', {
        'form': form,
        'title': f"Update {customer}"
    })
    
@login_required
@user_passes_test(is_manager, login_url='login_user')
def delete_customer(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        customer.delete()
        messages.success(request, "Customer deleted.")
        return redirect('sale_list')
    return render(request, 'sales/delete_customer.html', {
        'customer': customer,
        'title': f"Delete {customer}"
    })
    
def sales_dashboard(request):
    return render(request, 'sales/dashboard.html')