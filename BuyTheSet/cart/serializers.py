from decimal import Decimal
from icecream import ic
from .models import Cart, CartItem
from payments.models import Order

class CartSerializer:
    @staticmethod
    def get_cart_items(cart):
        return cart.cartitem_set.all()

    @staticmethod
    def get_cart_total(cart):
        cart_items = CartSerializer.get_cart_items(cart)
        total = sum(
            item.product.sale_price * item.quantity if item.product.is_sale 
            else item.product.price * item.quantity 
            for item in cart_items
        )
        shipping_fee = Decimal(Order._meta.get_field('shipping_fee').default)

        return total + shipping_fee
    
    @staticmethod
    def get_item_quantity(cart, product_id):
        cart_item = cart.cartitem_set.filter(product_id=product_id).first()
        if cart_item:
            return cart_item.quantity
        return 0
    
    @staticmethod
    def update_item_quantity(cart, product_id, quantity):
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product_id=product_id)
        product = cart_item.product
        if quantity > product.quantity:
            quantity = product.quantity
        cart_item.quantity = quantity
        cart_item.save()
        
    
    @staticmethod
    def remove_item(cart, product_id):
        cart_item = cart.cartitem_set.filter(product_id=product_id).first()
        if cart_item:
            cart_item.delete()
