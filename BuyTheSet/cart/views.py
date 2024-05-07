import json
from icecream import ic
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
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


def cart_add(request):
    if request.method == 'POST':
        cart = CartManager(request)
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get("product_qty"))
        try:
            CartSerializer.update_item_quantity(cart.cart, product_id, product_qty)
            cart_quantity = cart.get_total_quantity()
            response = {'success': True, 'cart_quantity': cart_quantity}
        except Product.DoesNotExist:
            response = {'success': False, 'error': 'Product does not exist.'}
        except Exception as e:
            response = {'success': False, 'error': str(e)}
        return JsonResponse(response)


def cart_items(request):
    cart = CartManager(request)
    cart_items = CartSerializer.get_cart_items(cart.cart)
    cart_total = CartSerializer.get_cart_total(cart.cart)
    cart_items_data = []
    for item in cart_items:
        item_data = {
            'product': {
                'id': item.product.id,
                'name': item.product.name,
                'price': str(item.product.price),
                'sale_price': str(item.product.sale_price),
                'is_sale': item.product.is_sale,
                'quantity': item.product.quantity,
                'image_url': item.product.image.url,
            },
            'quantity': item.quantity,
        }
        cart_items_data.append(item_data)
    data = {
        'cart_items': cart_items_data,
        'cart_total': str(cart_total),
    }
    return JsonResponse(data)


def cart_delete(request):
    cart = CartManager(request)
    if request.method == 'POST':
        data = json.loads(request.body)
        product_id = data.get('product_id')
        try:
            product = Product.objects.get(id=product_id)
            CartSerializer.remove_item(cart.cart, product_id)
            cart_quantity = cart.get_total_quantity()
            response = JsonResponse({'success': True, 'cart_quantity': cart_quantity})
        except Product.DoesNotExist:
            response = JsonResponse({'success': False, 'error': 'Product does not exist.'}, status=404)
        except Exception as e:
            response = JsonResponse({'success': False, 'error': str(e)}, status=500)
        return response
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request.'}, status=400)


@csrf_exempt
def cart_update(request):
    cart = CartManager(request)
    if request.method == 'POST':
        data = json.loads(request.body)
        product_id = data.get('product_id')
        quantity = data.get('quantity')
        try:
            product = Product.objects.get(id=product_id)
            CartSerializer.update_item_quantity(cart.cart, product_id, quantity)
            response = JsonResponse({'success': True})
        except Product.DoesNotExist:
            response = JsonResponse({'success': False, 'error': 'Product not found.'}, status=404)
        except Exception as e:
            response = JsonResponse({'success': False, 'error': str(e)}, status=500)
        return response
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request.'}, status=400)

