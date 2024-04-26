from django.shortcuts import render, redirect
from .forms import PaymentForm, ShippingAddressForm
from .serializers import ShippingAddressSerializer, PaymentSerializer
from cart.cart import CartManager
from cart.serializers import CartSerializer
from icecream import ic

        
def checkout(request):
    user = request.user
    cart = CartManager(request)
    initial_data = {}
    shipping_address = None
    if user.is_authenticated:
        shipping_address = ShippingAddressSerializer.get_user_shipping_address(user)
        if shipping_address:
            initial_data = ShippingAddressSerializer.get_initial_data_from_shipping_address(shipping_address)
        else:
            initial_data = ShippingAddressSerializer.get_initial_data_from_user_profile(user)
    else:
        initial_data = request.session.get('guest_shipping_address', {})
    form = ShippingAddressForm(request.POST or None, instance=shipping_address, initial=initial_data)
    if request.method == 'POST' and form.is_valid():
        ShippingAddressSerializer.save_shipping_address(form, user, request)
        return redirect('home')
    cart_items_data = PaymentSerializer.get_cart_items_data(cart.cart)
    cart_total = PaymentSerializer.get_cart_total(cart.cart)
    context = {
        'form': form,
        'cart_items_data': cart_items_data,
        'cart_total': cart_total,
    }
    return render(request, 'checkout.html', context)    
    
    

def process_payment(request):
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            # Do something with the form data
            return redirect('payment_success')
    else:
        form = PaymentForm()
    return render(request, 'process_payment.html', {'form': form})

def payment_success(request):
    return render(request, 'payment_success.html')


