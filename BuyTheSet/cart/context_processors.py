from .cart import CartManager

def get_cart(request):
    cart=CartManager(request)
    return {'cart': cart, 'cart_quantity': cart.__len__()}