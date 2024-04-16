from django.contrib import admin
from .models import Category, Customer,  Product, Order


models = [Category, Customer, Product, Order]

admin.site.register(models)

