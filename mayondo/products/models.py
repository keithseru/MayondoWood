from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length = 100)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name
    
class Unit(models.Model):
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name
    
class Product(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    unit = models.ForeignKey(Unit, on_delete=models.SET_NULL, null=True)
    price = models.IntegerField()
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name
    
    