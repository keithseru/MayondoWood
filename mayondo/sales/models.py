from django.db import models
from products.models import ProductVariant
from users.models import Employee

class Customer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Sale(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    sale_date = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Sale {self.id} to {self.customer} on {self.sale_date.strftime('%Y-%m-%d %H:%M')}"

    def total_amount(self):
        return sum(item.total_price() for item in self.items.all())

    @property
    def total(self):
        return self.total_amount()

class SaleItem(models.Model):
    sale = models.ForeignKey(Sale, related_name='items', on_delete=models.CASCADE)
    product_variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    def total_price(self):
        return self.quantity * self.unit_price

    def __str__(self):
        return f"{self.quantity} x {self.product_variant} at {self.unit_price} each"