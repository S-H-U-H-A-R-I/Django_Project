from .cart import CartManager

def get_cart(request):
    return {'cart': CartManager(request)}