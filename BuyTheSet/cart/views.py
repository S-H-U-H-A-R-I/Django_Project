from icecream import ic
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.template.loader import render_to_string
from .models import Cart, CartItem
from .cart import CartManager
from .serializers import CartSerializer
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
    cart = CartManager(request)
    cart_items = CartSerializer.get_cart_items(cart.cart)
    cart_total = CartSerializer.get_cart_total(cart.cart)
    alert_message = request.GET.get('alert_message')
    alert_type = request.GET.get('alert_type')
    context = {
        'cart_items': cart_items,
        'cart_total': cart_total,
        'alert_message': alert_message,
        'alert_type': alert_type,
    }
    return render(request, 'cart_summary.html', context)


def cart_add(request):
    if request.method == 'POST':
        cart = CartManager(request)
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get("product_qty"))
        try:
            product = Product.objects.get(id=product_id)
            CartSerializer.update_item_quantity(cart.cart, product_id, product_qty)
            success_message = f'{product.name} has been added to your cart.'
            response = {'success': True, 'product_name': product.name, 'message': success_message}
        except Product.DoesNotExist:
            response = {'success': False, 'error': 'Product does not exist.'}
        except Exception as e:
            response = {'success': False, 'error': str(e)}
        return JsonResponse(response)

def cart_delete(request):
    if request.method == 'POST':
        cart = CartManager(request)
        product_id = int(request.POST.get('product_id'))
        try:
            product = Product.objects.get(id=product_id)
            CartSerializer.remove_item(cart.cart, product_id)
            success_message = f'{product.name} has been removed from your cart.'
            response = {'success': True, 'message': success_message}
        except Product.DoesNotExist:
            response = {'success': False, 'error': 'Product does not exist.'}
        except Exception as e:
            response = {'success': False, 'error': str(e)}
        return JsonResponse(response)


def cart_update(request):
    cart = CartManager(request)
    if request.method == 'POST':
        try:
            product_id = int(request.POST.get('product_id'))
            product_qty = int(request.POST.get("product_qty"))
            product = Product.objects.get(id=product_id)
            CartSerializer.update_item_quantity(cart.cart, product_id, product_qty)
            success_message = f'{product.name} has been updated.'
            response = JsonResponse({'success': True, 'message': success_message})
            return response
        except ValueError:
            return JsonResponse({'success': False, 'error': 'Invalid quantity.'}, status=400)
        except ObjectDoesNotExist:
            return JsonResponse({'success': False, 'error': 'Product not found.'}, status=404)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request.'}, status=400)

