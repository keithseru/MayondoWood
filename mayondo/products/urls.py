from django.urls import path
from . import views

urlpatterns = [
    # Inventory listing (visible to all roles)
    path("", views.product_list, name="product_list"),

    # Product CRUD (manager only)
    path("create/", views.create_product, name="create_product"),
    path("update/<int:pk>/", views.update_product, name="update_product"),
    path("detail/<int:pk>/", views.product_detail, name="product_detail"),

    # Category and Unit creation (manager only)
    path("category/create/", views.create_category, name="create_category"),
    path("unit/create/", views.create_unit, name="create_unit"),
]