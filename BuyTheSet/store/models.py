from django.db import models
from django.utils import timezone

class Category(models.Model):
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'categories'


class Customer(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True, blank=False)
    password = models.CharField(max_length=255, blank=False)

    class Meta:
        verbose_name = 'customer'
        verbose_name_plural = 'customers'
        
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return f"{self.full_name} - {self.email}" 


class Product(models.Model):
    name  = models.CharField(max_length=255, blank=False)
    price =  models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='uploads/products/', default='no-image.jpg')
    
    is_sale = models.BooleanField(default=False)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    class Meta:
        verbose_name = 'product'
        verbose_name_plural = 'products'
        
    def __str__(self):
        return self.name
    

    
    

class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    address = models.CharField(max_length=255, default='',  blank=False)
    phone = models.CharField(max_length=50, default='', blank=True)
    date = models.DateField(default=timezone.now)
    status = models.BooleanField(default=False)
    
    def __str__(self):
        return str(self.product.name)