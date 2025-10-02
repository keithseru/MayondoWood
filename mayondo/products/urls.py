from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('create/', views.create_product, name='create_product'),
    path('<int:pk>/', views.product_detail, name='product_detail'),
    path('<int:pk>/update/', views.update_product, name='update_product'),
    path('<int:pk>/delete/', views.delete_product, name='delete_product'),
    path('create-category/', views.create_category, name='create_category'),
    path('create-unit/', views.create_unit, name='create_unit'),
]