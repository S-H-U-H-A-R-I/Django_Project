from django.contrib import admin
from .models import Category, Customer,  Product, Order, Profile
from django.contrib.auth.models import User


models = [Category, Customer, Product, Order, Profile]

admin.site.register(models)

# Mix Profile info and User info
class ProfileInline(admin.StackedInline):
    model = Profile


# Extend User model
class UserAdmin(admin.ModelAdmin):
    model = User
    fields = ['username', 'email', 'first_name', 'last_name']
    inlines = [ProfileInline]
    
# unregister the User model
admin.site.unregister(User)

# re-register the User model
admin.site.register(User, UserAdmin)