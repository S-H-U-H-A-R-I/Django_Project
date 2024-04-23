from django.contrib import admin
from django.contrib import messages
from .models import Cart, CartItem


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    fields = ['product', 'quantity', 'created_at']
    readonly_fields = ['product', 'created_at']


def empty_cart(modeladmin, request, queryset):
    for cart in queryset:
        cart.cartitem_set.all().delete()
        messages.success(request, f"Selected carts emptied")
empty_cart.short_description = "Empty selected carts"


class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_total_items', 'created_at')
    list_filter = ('user',)
    actions = [empty_cart]
    inlines = [CartItemInline]
    search_fields = ['user__username']
    
    def get_total_items(self, obj):
        return obj.cartitem_set.count()
    get_total_items.short_description = "Total Items"
    
    def created_at(self, obj):
        return obj.created_at.strftime('%Y-%m-%d %H:%M')
    created_at.admin_order_field = "created_at"
    created_at.short_description = "Created At"
    
    
admin.site.register(Cart, CartAdmin)