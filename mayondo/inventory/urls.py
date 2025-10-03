from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.inventory_dashboard, name='inventory_dashboard'),
    path('', views.stock_entry_list, name='stock_list'),
    path('create/', views.create_stock_entry, name='create_stock'),
]
