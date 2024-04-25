from django.contrib import admin
from .models import ShippingAddress, Order, OrderItem


@admin.register(ShippingAddress)
class ShippingAddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'email', 'address1', 'address2')
    search_fields = ('user__username', 'full_name', 'email')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'full_name', 'email', 'amount_paid', 'date_ordered')
    search_fields = ('user__username', 'full_name', 'email')
    date_hierarchy = 'date_ordered'
    
    
@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'user', 'quantity', 'price')
    search_fields = ('order__id', 'product__name', 'user__username')