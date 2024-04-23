from store.models import Product
from .models import Cart, CartItem
from icecream import ic


class CartManager:
    def __init__(self, request):
        self.session = request.session
        self.user = request.user
        if self.user.is_authenticated:
            self.cart, _ = Cart.objects.get_or_create(user=self.user)
        else:
            cart_id = self.session.get('cart_id')
            if cart_id:
                self.cart = Cart.objects.filter(id=cart_id, user=None).first()
            if not cart_id or not self.cart:
                self.cart = Cart.objects.create(user=None)
                self.session['cart_id'] = self.cart.id
            
    def add(self, product, quantity):
        if self.cart:
            try:
                cart_item = CartItem.objects.get(cart=self.cart, product=product)
                cart_item.quantity = quantity
                cart_item.save()
            except CartItem.DoesNotExist:
                CartItem.objects.create(cart=self.cart, product=product, quantity=quantity)
        
    def __len__(self):
        """
        This method returns the length of the user's cart.
        The `len` method is a special method in Python that is called when the built-in `len` function is used on an instance of this class.
        By implementing this method, we can define the behavior of `len` for instances of this class.
        In this case, we return the length of the `cart` attribute, which is a list of items in the user's cart.
        """
        if self.cart:
            return self.cart.cartitem_set.count()
        return 0
    
    def get_products(self):
        if self.cart:
            return [item.product for item in self.cart.cartitem_set.all()]
        return []
    
    def get_quantity(self):
        if self.cart:
            return {str(item.product.id): item.quantity for item in self.cart.cartitem_set.all()}
        return {}

    def cart_total(self):
        if self.cart:
            total = 0
            for item in self.cart.cartitem_set.all():
                product = item.product
                quantity = item.quantity
                if product.is_sale:
                    total += product.sale_price * quantity
                else:
                    total += product.price * quantity
            return total
        return 0
    
    def update(self, product, quantity):
        if self.cart:
            try:
                cart_item = CartItem.objects.get(cart=self.cart, product=product)
                if quantity > 0:
                    cart_item.quantity = quantity
                    cart_item.save()
                else:
                    cart_item.delete()
            except CartItem.DoesNotExist:
                if quantity > 0:
                    CartItem.objects.create(cart=self.cart, product=product, quantity=quantity)
    
    def delete(self, product):
        if self.cart:
            try:
                cart_item = CartItem.objects.get(cart=self.cart, product=product)
                cart_item.delete()
            except CartItem.DoesNotExist:
                pass
            
        