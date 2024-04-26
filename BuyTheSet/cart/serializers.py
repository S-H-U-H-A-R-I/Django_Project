from .models import Cart, CartItem

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
        return total
    
    @staticmethod
    def get_item_quantity(cart, product_id):
        cart_item = cart.cartitem_set.filter(product_id=product_id).first()
        if cart_item:
            return cart_item.quantity
        return 0
    
    @staticmethod
    def update_item_quantity(cart, product_id, quantity):
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product_id=product_id)
        cart_item.quantity = quantity
        cart_item.save()
        
    
    @staticmethod
    def remove_item(cart, product_id):
        cart_item = cart.cartitem_set.filter(product_id=product_id).first()
        if cart_item:
            cart_item.delete()
