from django.db import models
from users.models import Employee

# Create your models here.

class Supplier(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    contact_person = models.CharField(max_length=100)
    address = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    
    def __str__(self):
        return self.name
    
class Order(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT)
    order_date = models.DateField(auto_now_add=True)
    expected_delivery = models.DateField(null=True, blank=True)
    created_by = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True)
    received_by = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, related_name='confirmed_orders')
    received_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=[
        ('PENDING', 'Pending'),
        ('DELIVERED', 'Delivered'),
        ('PARTIAL', 'Partial'),
        ('CANCELLED', 'Cancelled'),
    ], default='PENDING')
    
    def __str__(self):
        return f"Order #{self.id} - {self.supplier.name}"
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    variant = models.ForeignKey('products.ProductVariant', on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    delivered_quantity = models.PositiveIntegerField(default=0)
    unit_price = models.IntegerField()
    is_delivered = models.BooleanField(default=False)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.variant} - {self.quantity} ordered, {self.delivered_quantity} received"
