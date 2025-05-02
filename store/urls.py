from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('order/<int:pk>/', views.order_create, name='order_create'),
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
]