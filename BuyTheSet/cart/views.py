from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .cart import Cart
from store.models import Product


def cart_summary(request):
    cart = Cart(request) # Initialize the cart object using the Cart class and the request object
    cart_products = cart.get_products() # Get the list of products in the cart using the get_products method
    quantities = cart.get_quantity() # Get the quantities of each product in the cart using the get_quantity method
    totals = cart.cart_total()

    context = {
        "cart_products":cart_products,
        "quantities" : quantities,
        "totals" : totals
    }
    return render(request, "cart_summary.html", context)


def cart_add(request):
    # Check if the request method is POST
    if request.method == 'POST':
        # Initialize the cart object with the current request
        cart = Cart(request)
        
        # Get the product ID from the POST data
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get("product_qty"))
        
        # Retrieve the product object from the database using the product ID
        product = get_object_or_404(Product, id=product_id)
        
        # Add the product to the cart
        cart.add(product=product, quantity=product_qty)
        
        # Get cart quantity
        cart_quantity = cart.__len__()
        
        # Prepare the response data with the product name
        response = {'qty': cart_quantity}
        
        # Return the response data as a JSON object
        return JsonResponse(response)


def cart_delete(request):
    cart = Cart(request)
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
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        try:
            product_id = int(request.POST.get('product_id'))
            product_qty = int(request.POST.get('product_qty'))
            # validate if the product exists
            Product.objects.get(id=product_id)  
            cart.update(product=product_id, quantity=product_qty)
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
