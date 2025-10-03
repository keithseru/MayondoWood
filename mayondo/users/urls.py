from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_user, name='login_user'),
    path('logout/', views.logout_user, name='logout_user'),
    path('create_staff/', views.create_staff, name='create_staff'),
    path('staff_list/', views.staff_list, name='staff_list'),
    path('profile/', views.profile_view, name='profile_view'),
    path('dashboard/', views.dashboard_router, name='dashboard_router'),
]
