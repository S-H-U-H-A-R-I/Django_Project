from django.contrib import admin
from .models import Cart, CartItem


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0


def empty_cart(modeladmin, request, queryset):
    for cart in queryset:
        cart.cartitem_set.all().delete()
empty_cart.short_description = "Empty selected carts"


class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_total_items')
    actions = [empty_cart]
    inlines = [CartItemInline]
    
    def get_total_items(self, obj):
        return obj.cartitem_set.count()
    get_total_items.short_description = "Total Items"
    
    
admin.site.register(Cart, CartAdmin)