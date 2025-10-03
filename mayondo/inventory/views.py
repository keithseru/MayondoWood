from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import StockEntryForm
from .models import StockEntry

# Create your views here.
def is_manager(user):
    return user.is_authenticated and user.role == 'MANAGER'

def is_inventory_or_manager(user):
    return user.is_authenticated and user.role in ['INVENTORY', 'MANAGER']

@login_required
@user_passes_test(is_inventory_or_manager, login_url='login_user')
def create_stock_entry(request):
    if request.method == 'POST':
        form = StockEntryForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.entered_by = request.user
            entry.save()
            return redirect('stock_list')
    else:
        form = StockEntryForm()
    
    context = {'form': form}
    return render(request, 'inventory/stock_entry.html', context)

@login_required
@user_passes_test(is_inventory_or_manager)
def stock_entry_list(request):
    entries = StockEntry.objects.select_related('variant', 'entered_by').order_by('-entry_date')
    context = {'entries': entries}
    return render(request, 'inventory/stock_list.html', context)
