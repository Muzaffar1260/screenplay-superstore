from django.db import models

# Create your models here.
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)  # e.g., '2009'

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"  # Fix plural name

class Product(models.Model):
    name = models.CharField(max_length=200)  # Movie title
    description = models.TextField()  # Generated
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Derived from Gross
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    location = models.CharField(max_length=200, blank=True)  # Placeholder
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Order(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    order_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"