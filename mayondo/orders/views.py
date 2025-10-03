from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from datetime import datetime
from .models import Order, Supplier
from .forms import OrderForm, OrderItemFormSet, DeliveryFormSet, SupplierForm
from inventory.models import StockEntry

def is_manager(user):
    return user.is_authenticated and user.role == 'MANAGER'

def is_manager_or_clerk(user):
    return user.is_authenticated and user.role in ['INVENTORY', 'MANAGER']

# Orders
@login_required
@user_passes_test(is_manager_or_clerk, login_url='login_user')
def order_list(request):
    orders = Order.objects.select_related('supplier', 'created_by', 'received_by').prefetch_related('items__variant')
    return render(request, 'orders/order_list.html', {
        'orders': orders,
        'title': 'Order List'
    })

@login_required
@user_passes_test(is_manager, login_url="login_user")
def create_order(request):
    if request.method == "POST":
        form = OrderForm(request.POST)
        formset = OrderItemFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            order = form.save(commit=False)
            order.created_by = request.user
            order.save()
            formset.instance = order
            formset.save()
            messages.success(request, "Order created successfully.")
            return redirect('order_detail', pk=order.pk)
    else:
        form = OrderForm()
        formset = OrderItemFormSet()

    context = {
        'form': form,
        'formset': formset,
        'title': 'Create Order'
    }
    return render(request, 'orders/create_order.html', context)

@login_required
@user_passes_test(is_manager_or_clerk, login_url="login_user")
def confirm_delivery(request, pk):
    order = get_object_or_404(Order, pk=pk)
    formset = DeliveryFormSet(queryset=order.items.all())

    if request.method == 'POST':
        formset = DeliveryFormSet(request.POST, queryset=order.items.all())
        if formset.is_valid():
            formset.save()

            all_delivered = True
            for item in order.items.all():
                if item.delivered_quantity > 0:
                    item.is_delivered = item.delivered_quantity >= item.quantity
                    item.save()
                    StockEntry.objects.create(
                        variant=item.variant,
                        quantity=item.delivered_quantity,
                        entry_type="IN",
                        recorded_by=request.user
                    )
                if item.delivered_quantity < item.quantity:
                    all_delivered = False

            order.status = 'DELIVERED' if all_delivered else 'PARTIAL'
            order.received_by = request.user
            order.received_date = datetime.now()
            order.is_fully_delivered = all_delivered
            order.save()
            messages.success(request, "Delivery confirmed.")
            return redirect('order_detail', pk=order.pk)

    context = {
        'order': order,
        'formset': formset,
        'title': 'Confirm Delivery'
    }
    return render(request, 'orders/confirm_delivery.html', context)

@login_required
@user_passes_test(is_manager_or_clerk, login_url="login_user")
def order_detail(request, pk):
    order = get_object_or_404(Order.objects.prefetch_related('items__variant'), pk=pk)
    return render(request, 'orders/order_detail.html', {
        'order': order,
        'title': f"Order #{order.id} Details"
    })

# Suppliers   
@login_required
@user_passes_test(is_manager_or_clerk, login_url='login_user')
def supplier_list(request):
    suppliers = Supplier.objects.all().order_by('name')
    return render(request, 'orders/supplier_list.html', {
        'suppliers': suppliers,
        'title': 'Supplier List'
    })
    
@login_required
@user_passes_test(is_manager_or_clerk, login_url='login_user')
def create_supplier(request):
    if request.method == 'POST':
        form = SupplierForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Supplier added successfully.")
            return redirect('supplier_list')
    else:
        form = SupplierForm()
    return render(request, 'orders/create_supplier.html', {
        'form': form,
        'title': 'Add Supplier'
    })
    
@login_required
@user_passes_test(lambda u: u.role in ['INVENTORY', 'MANAGER'], login_url='login_user')
def update_supplier(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    if request.method == 'POST':
        form = SupplierForm(request.POST, instance=supplier)
        if form.is_valid():
            form.save()
            messages.success(request, "Supplier updated successfully.")
            return redirect('supplier_list')
    else:
        form = SupplierForm(instance=supplier)
    return render(request, 'orders/update_supplier.html', {
        'form': form,
        'title': f"Edit Supplier: {supplier.name}"
    })

@login_required
@user_passes_test(lambda u: u.role in ['INVENTORY', 'MANAGER'], login_url='login_user')
def delete_supplier(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    if request.method == 'POST':
        supplier.delete()
        messages.success(request, "Supplier deleted.")
        return redirect('supplier_list')
    return render(request, 'orders/delete_supplier.html', {
        'supplier': supplier,
        'title': f"Delete Supplier: {supplier.name}"
    })

