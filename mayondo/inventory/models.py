from django.db import models
from products.models import ProductVariant
from users.models import Employee

# Create your models here.
class StockEntry(models.Model):
    variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    entry_date = models.DateField(auto_now_add=True)
    entered_by = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True)
    notes = models.TextField(blank=True)
    
    def __str__(self):
        return f'{self.variant} - {self.quantity} units'