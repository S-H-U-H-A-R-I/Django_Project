import requests
from icecream import ic
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render, redirect
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
    

def payment_success(request):
    cart = CartManager(request)
    # Retrieve the shipping address
    shipping_address = None
    if request.user.is_authenticated:
        shipping_address = ShippingAddressSerializer.get_user_shipping_address(request.user)
    else:
        guest_shipping_address_id = request.session.get('guest_shipping_address_id')
        if guest_shipping_address_id:
            shipping_address = ShippingAddress.objects.get(id=guest_shipping_address_id)
    if shipping_address:
        # Create an order
        order = Order.objects.create(
            user=request.user if request.user.is_authenticated else None,
            full_name=shipping_address.full_name,
            email=shipping_address.email,
            shipping_address=f"{shipping_address.address1}, {shipping_address.address2}",
            amount_paid=PaymentSerializer.get_cart_total(cart.cart),
        )
        # Create order items for each item in the cart
        for item in cart.cart.cartitem_set.all():
            OrderItem.objects.create(
                order=order,
                product=item.product,
                user=request.user if request.user.is_authenticated else None,
                quantity=item.quantity,
                price=item.product.sale_price if item.product.is_sale else item.product.price,
            )
            cart.clear()
    return render(request, 'payment_success.html')

