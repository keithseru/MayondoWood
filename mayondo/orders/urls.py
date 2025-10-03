from django.urls import path
from . import views

urlpatterns = [
    path('suppliers/', views.supplier_list, name='supplier_list'),
    path('suppliers/create/', views.create_supplier, name='create_supplier'),
    path('suppliers/<int:pk>/edit/', views.update_supplier, name='update_supplier'),
    path('suppliers/<int:pk>/delete/', views.delete_supplier, name='delete_supplier'),
    
    path('', views.order_list, name='order_list'),
    path('create/', views.create_order, name='create_order'),
    path('<int:pk>/confirm/', views.confirm_delivery, name='confirm_delivery'),
    path('<int:pk>/', views.order_detail, name='order_detail'),
]
