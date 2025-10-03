from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from datetime import datetime
from .models import Order, OrderItem
from .forms import OrderForm, OrderItemFormSet, DeliveryFormSet
from inventory.models import StockEntry

def is_manager(user):
    return user.is_authenticated and user.role == 'MANAGER'

def is_manager_or_clerk(user):
    return user.is_authenticated and user.role in ['INVENTORY', 'MANAGER']

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