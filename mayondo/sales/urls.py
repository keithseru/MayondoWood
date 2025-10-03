from django.urls import path
from . import views

urlpatterns = [
    path('dashboard', views.sales_dashboard, name='sales_dashboard'),
    path('', views.sale_list, name='sale_list'),
    path('create/', views.create_sale, name='create_sale'),
    path('<int:pk>/', views.sale_detail, name='sale_detail'),
    path('customers/', views.customer_list, name='customer_list'),
    path('customer/create/', views.create_customer, name='create_customer'),
    path('customer/<int:pk>/update/', views.update_customer, name='update_customer'),
    path('customer/<int:pk>/delete/', views.delete_customer, name='delete_customer'),
    path('<int:pk>/update/', views.update_sale, name='update_sale'),
    path('<int:pk>/delete/', views.delete_sale, name='delete_sale'),

]