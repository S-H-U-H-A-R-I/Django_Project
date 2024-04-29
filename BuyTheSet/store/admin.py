from typing import Any
from django.contrib import admin
from django.contrib.admin.options import InlineModelAdmin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.http import HttpRequest
from .models import Category, Product, ProductImage, Profile


class ProfileInLine(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'profile'
    fk_name = 'user'


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    list_select_related = ('profile',)
    inlines = [ProfileInLine,]
    
    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(UserAdmin, self).get_inline_instances(request, obj)
    
    
# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


# Admin for Product with additional features
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'cost_price', 'price', 'category', 'is_sale', 'sale_price', 'quantity', 'profit')
    list_filter = ('is_sale', 'category')
    search_fields = ('name', 'description')
    list_editables = ('cost_price', 'price', 'is_sale', 'sale_price', 'quantity')
    inlines = [ProductImageInline,]
    
    def profit(self, obj):
        return obj.profit
    profit.short_description = 'Profit'
    
    
admin.site.register(Product, ProductAdmin)
admin.site.register(Category)