import html
import json
import re
from decimal import Decimal
from icecream import ic
from django.conf import settings
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
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
    default_shipping_fee = Order._meta.get_field('shipping_fee').default
    context = {
        'form': form,
        'cart_items_data': cart_items_data,
        'cart_total': cart_total,
        'paystack_public_key': paystack_public_key,
        'default_shipping_fee': default_shipping_fee,
    }
    return render(request, 'checkout.html', context)    

    
def save_shipping_info(request):
    if request.method == 'POST':
        is_collect = request.POST.get('is_collect') == "True"
        if is_collect:
            # Validate required fields
            required_fields = ['full_name', 'email', 'phone_number']
            errors = {}
            for field in required_fields:
                if not request.POST.get(field):
                    errors[field] = f'{field.replace("_", " ").capitalize()} is required.'
            # Validate email
            email = request.POST.get('email')
            if email and not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
                errors['email'] = 'Invalid email address.'
            # Validate phone number
            phone_number = request.POST.get('phone_number')
            if phone_number and not re.match(r'^\+?1?\d{9,15}$', phone_number):
                errors['phone_number'] = 'Invalid phone number.'
            if errors:
                return JsonResponse({'success': False, 'errors': errors})
            else:
                return JsonResponse({'success': True})
        else:
            form = ShippingAddressForm(request.POST)
            if form.is_valid():
                ShippingAddressSerializer.save_shipping_address(form, request.user, request)
                return JsonResponse({'success': True})
            else:
                errors = {field: error[0] for field, error in form.errors.items()}
                return JsonResponse({'success': False, 'errors': errors})
    return JsonResponse({'success': False, 'errors': 'Invalid request'})
    

def check_product_availability(request):
    if request.method == 'POST':
        products_data = json.loads(request.POST.get('products'))
        for product_data in products_data:
            product_name = html.unescape(product_data['name'])
            quantity = product_data['quantity']
            product = get_object_or_404(Product, name=product_name)
            if product.quantity < quantity:
                return JsonResponse({'success': False, 'error': f'Insufficient quantity for product: {product_name}'})
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'error': 'Invalid request'})


@csrf_exempt
def save_order(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        amount = request.POST.get('amount')
        products_data = json.loads(request.POST.get('products'))
        shipping_address = request.POST.get('shipping_address', '')
        is_collect = request.POST.get('is_collect') == 'true'
        
        with transaction.atomic():
            # Create a new Order instance
            order = Order.objects.create(
                user=request.user if request.user.is_authenticated else None,
                full_name=f'{first_name} {last_name}',
                email=email,
                shipping_address='' if is_collect else shipping_address,
                amount_paid=Decimal(amount) / 100,
                is_collect=is_collect,
            )
            # Create OrderItem instances for each purchased product
            for product_data in products_data:
                product_name = html.unescape(product_data['name'])
                quantity = product_data['quantity']
                price = product_data['price']
                total = product_data['total']
                # Retrieve the corresponding Product instance based on the product name
                product = get_object_or_404(Product, name=product_name)
                if product.quantity >= quantity:
                    product.quantity -= quantity
                    product.save()
                else:
                    return JsonResponse({'success': False, 'errors': 'Insufficient quantity for product.'})
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

