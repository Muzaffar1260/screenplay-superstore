from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Category, Product, Order

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)  # Display the 'name' field in the list view
    search_fields = ('name',)  # Add a search bar for the 'name' field

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category', 'created_at')  # Display these fields
    list_filter = ('category', 'created_at')  # Add filters for category and creation date
    search_fields = ('name', 'description')  # Search by name or description
    list_per_page = 25  # Show 25 products per page

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'quantity', 'order_date')  # Display these fields
    list_filter = ('order_date',)  # Filter by order date
    search_fields = ('user__username', 'product__name')  # Search by username or product name