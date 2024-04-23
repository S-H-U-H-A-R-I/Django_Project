from icecream import ic
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Cart, CartItem
from .cart import CartManager
from store.models import Product


@receiver(user_logged_in)
def merge_guest_cart(sender, user, request, **kwargs):
    guest_cart = request.session.get('cart_id')
    if guest_cart:
        try:
            guest_cart = Cart.objects.get(id=guest_cart)
            user_cart, _ = Cart.objects.get_or_create(user=user)
            for item in guest_cart.cartitem_set.all():
                user_item, created = CartItem.objects.get_or_create(cart=user_cart, product=item.product)
                user_item.quantity = item.quantity
                user_item.save()
            guest_cart.delete()
            del request.session['cart_id']
        except Cart.DoesNotExist:
            pass


def cart_summary(request):
    cart = CartManager(request) # Initialize the cart object using the Cart class and the request object
    cart_products = cart.get_products() # Get the list of products in the cart using the get_products method
    quantities = cart.get_quantity() # Get the quantities of each product in the cart using the get_quantity method
    totals = cart.cart_total()
    total_quantity = sum(quantities.values())

    context = {
        "cart_products":cart_products,
        "quantities" : quantities,
        "totals" : totals,
        "total_quantity" : total_quantity,
    }
    return render(request, "cart_summary.html", context)


def cart_add(request):
    # Check if the request method is POST
    if request.method == 'POST':
        # Initialize the cart object with the current request
        cart = CartManager(request)
        
        # Get the product ID from the POST data
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get("product_qty"))
        
        # Retrieve the product object from the database using the product ID
        product = get_object_or_404(Product, id=product_id)
        
        try:
            # Add the product to the cart
            cart.add(product=product, quantity=product_qty)
            # Get cart quantity
            cart_quantity = cart.__len__()
            response = {'success': True, 'qty': cart_quantity, 'product_name': product.name}
        except Exception as e:
            response = {'success': False, 'error': str(e)}
    
        # Return the response data as a JSON object
        return JsonResponse(response)


def cart_delete(request):
    cart = CartManager(request)
    if request.POST.get('action') == 'post':
        try:
            product_id = int(request.POST.get('product_id'))
            # validate if the product exists
            product = Product.objects.get(id=product_id)  
            cart.delete(product=product_id)
            messages.success(request, f"{product.name} has been deleted successfully.", "success")
            response = JsonResponse({'status': 'success'})
            return response
        except ValueError:
            # Handle the case where the input cannot be converted to an integer
            return JsonResponse({'error': 'Invalid input'}, status=400)
        except ObjectDoesNotExist:
            # Handle the case where the product does not exist
            return JsonResponse({'error': 'Product not found'}, status=404)
        except Exception as e:
            # Handle any other exceptions that may occur
            return JsonResponse({'error': str(e)}, status=500)


def cart_update(request):
    cart = CartManager(request)
    if request.POST.get('action') == 'post':
        try:
            product_id = int(request.POST.get('product_id'))
            product_qty = int(request.POST.get('product_qty'))
            # validate if the product exists
            product = Product.objects.get(id=product_id)  
            cart.update(product=product_id, quantity=product_qty)
            messages.success(request, f"{product.name} has been updated successfully.", "success")
            response = JsonResponse({'qty':product_qty})
            return response
        except ValueError:
            # Handle the case where the input cannot be converted to an integer
            return JsonResponse({'error': 'Invalid input'}, status=400)
        except ObjectDoesNotExist:
            # Handle the case where the product does not exist
            return JsonResponse({'error': 'Product not found'}, status=404)
        except Exception as e:
            # Handle any other exceptions that may occur
            return JsonResponse({'error': str(e)}, status=500)
    else:
        # Handle the case where the action is not 'post'
        return JsonResponse({'error': 'invalid action'}, status=400)
