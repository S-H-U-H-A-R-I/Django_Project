from django.shortcuts import render, redirect
from .forms import PaymentForm, ShippingAddressForm
from .serializers import ShippingAddressSerializer
from icecream import ic

def add_shipping_address(request):
    user = request.user
    initial_data = {}
    shipping_address = None
    if user.is_authenticated:
        # Retrieve the user's existing shipping addresss, if any
        shipping_address = ShippingAddressSerializer.get_user_shipping_address(user)
        if shipping_address:
            # If a shipping address exists, use its data as initial data for the form
            initial_data = ShippingAddressSerializer.get_initial_data_from_shipping_address(shipping_address)
        else:
            # If no shipping address exists, use the user's profile data as initial data for the form
            initial_data = ShippingAddressSerializer.get_initial_data_from_user_profile(user)
    else:
        # For guest users, retrieve the shipping address data from the session, if available
        initial_data = request.session.get('guest_shipping_address', {})
    # Create an instance of the ShippingAddressForm with the initial and the shipping address instance (if available)
    form = ShippingAddressForm(request.POST or None, instance=shipping_address, initial=initial_data)
    if request.method == 'POST' and form.is_valid():
        # if the request method is POST and the form is valid, save the shipping address
        ShippingAddressSerializer.save_shipping_address(form, user, request)
        return redirect('home')
    # Render the shipping address form template with the form as context
    return render(request, 'shipping_address.html', {'form': form})
    

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


