import html
import json
from decimal import Decimal
from icecream import ic
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from .forms import PaymentForm, ShippingAddressForm
from .models import ShippingAddress, Order, OrderItem
from .serializers import ShippingAddressSerializer, PaymentSerializer
from cart.cart import CartManager
from store.models import Product
        
        
def checkout(request):
    user = request.user
    cart = CartManager(request)
    if len(cart) == 0:
        return redirect('home')
    initial_data = {}
    shipping_address = None
    if user.is_authenticated:
        shipping_address = ShippingAddressSerializer.get_user_shipping_address(user)
        if shipping_address:
            initial_data = ShippingAddressSerializer.get_initial_data_from_shipping_address(shipping_address)
        else:
            initial_data = ShippingAddressSerializer.get_initial_data_from_user_profile(user)
    else:
        guest_shipping_address_id = request.session.get('guest_shipping_address_id')
        if guest_shipping_address_id:
            shipping_address = ShippingAddress.objects.get(id=guest_shipping_address_id)
            initial_data = ShippingAddressSerializer.get_initial_data_from_shipping_address(shipping_address)
    form = ShippingAddressForm(instance=shipping_address, initial=initial_data)
    cart_items_data = PaymentSerializer.get_cart_items_data(cart.cart)
    cart_total = PaymentSerializer.get_cart_total(cart.cart)
    paystack_public_key = settings.PAYSTACK_PUBLIC_KEY
    context = {
        'form': form,
        'cart_items_data': cart_items_data,
        'cart_total': cart_total,
        'paystack_public_key': paystack_public_key,
    }
    return render(request, 'checkout.html', context)    

    
def save_shipping_info(request):
    if request.method == 'POST':
        form = ShippingAddressForm(request.POST)
        if form.is_valid():
            ShippingAddressSerializer.save_shipping_address(form, request.user, request)
            return JsonResponse({'success': True})
        else:
            errors = {field: error[0] for field, error in form.errors.items()}
            return JsonResponse({'success': False, 'errors': errors})
    return JsonResponse({'success': False, 'errors': 'Invalid request'})
    

@csrf_exempt
def save_order(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        amount = request.POST.get('amount')
        products_data = json.loads(request.POST.get('products'))
        shipping_address = request.POST.get('shipping_address', '')
        # Create a new Order instance
        order = Order.objects.create(
            user=request.user if request.user.is_authenticated else None,
            full_name=f'{first_name} {last_name}',
            email=email,
            shipping_address=shipping_address,
            amount_paid=Decimal(amount) / 100
        )
        # Create OrderItem instances for each purchased product
        for product_data in products_data:
            product_name = html.unescape(product_data['name'])
            quantity = product_data['quantity']
            price = product_data['price']
            total = product_data['total']
            # Retrieve the corresponding Product instance based on the product name
            product = Product.objects.get(name=product_name)
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                price=price,
                user=request.user if request.user.is_authenticated else None,
            )
        cart = CartManager(request)
        cart.cart.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'errors': 'Invalid request'})


def payment_success(request):
    return render(request, 'payment_success.html')

