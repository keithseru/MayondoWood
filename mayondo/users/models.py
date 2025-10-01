from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Employee(AbstractUser):
    ROLES = [
        ('MANAGER', 'Manager'),
        ('SALES', 'Sales Agent'),
        ('INVENTORY', 'Inventory Clerk'),
    ]
    
    role = models.CharField(max_length=20, choices=ROLES)
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f'{self.username} - {self.role}'
