from typing import Any
from django.contrib import admin
from django.contrib.admin.options import InlineModelAdmin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.http import HttpRequest
from .models import Category, Customer,  Product, Order, Profile


admin.site.register([Category, Customer, Order])


class ProfileInLine(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'profile'
    fk_name = 'user'


class UserAdmin(admin.ModelAdmin):
    inlines = (ProfileInLine,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    list_select_related = ('profile',)
    
    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(UserAdmin, self).get_inline_instances(request, obj)
    
    
# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)


# Admin for Product with additional features
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category', 'is_sale', 'sale_price')
    list_filter = ('is_sale', 'category')
    search_fields = ('name', 'description')
    list_editables = ('price', 'is_sale','sale_price')
    
    
admin.site.register(Product, ProductAdmin)