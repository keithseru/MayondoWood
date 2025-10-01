from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.urls import reverse_lazy
from .forms import StaffForm, StaffAuthenticationForm
from .models import Employee


# Create your views here.
def is_manager(user):
    return user.is_authenticated and user.role == 'MANAGER'

# Login View
def login_user(request):
    if request.method == "POST":
        form = StaffAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.role in ["MANAGER", "SALES", "INVENTORY"]:
                login(request, user)
                return redirect('dashboard_router') 
            else:
                messages.error(request, 'You are not authorized to access the system')
                return redirect('login_user')
    else:
        form = StaffAuthenticationForm()
    
    context = {
        'form' : form,
        'title' : 'Login'
        }
    return render(request, 'login.html', context) 

#Logout View
@login_required
def logout_user(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('login_user')

#Staff Creation (manager only)
@user_passes_test(is_manager, login_url=reverse_lazy('login_user'))
def create_staff(request):
    if request.method == 'POST':
        form = StaffForm(request.POST)
        if form.is_valid():
            staff = form.save()
            messages.success(request, f'Staff account created successfully. Username: {staff.username}')
            return redirect('manager_dashboard')
    
    context = {
        'form': form,
        'title': 'Create Staff Account'
    }
    return render(request, 'users/create_staff.html', context)

# Profile View
@login_required
def profile_view(request):
    return render(request, 'users/profile.html', {'user': request.user})

#Dashboard Redirect
def dashboard_router(request):
    role = request.user.role
    if role == 'MANAGER':
        return redirect('manager_dashboard')
    elif role == 'SALES':
        return redirect('sales_dashboard')
    elif role == 'INVENTORY':
        return redirect('inventory_dashboard')
    else:
        messages.error(request, 'Invalid role. Contact admin')
        return redirect('login_user')