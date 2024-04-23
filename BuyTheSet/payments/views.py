from django.shortcuts import render, redirect
from .forms import PaymentForm, ShippingAddressForm
from .models import ShippingAddress
from store.models import Profile


def add_shipping_address(request):
    initial_data = {}
    shipping_address = None
    if request.user.is_authenticated:
        # Try to fetch an existing shipping address for the user
        shipping_address = ShippingAddress.objects.filter(user=request.user).first()
        if shipping_address:
            # if a shipping address exists, use it to pre-populate the form
            initial_data = {
                'full_name': shipping_address.full_name,
                'email': shipping_address.email,
                'address1': shipping_address.address1,
                'address2': shipping_address.address2,
                'phone_number': shipping_address.phone_number,
            }
        else:
            # if no shipping address exists, pre-populate the form with the user's profile
            profile = Profile.objects.filter(user=request.user).first()
            if profile:
                initial_data = {
                    'full_name': request.user.get_full_name(),
                    'email': profile.email,
                    'phone_number': profile.phone_number,
                    'address1': profile.address1,
                    'address2': profile.address2,
                }
    else:
        # Load initial data from session if available (for guests)
        initial_data = request.session.get('guest_shipping_address', {})
    form = ShippingAddressForm(request.POST or None, instance=shipping_address, initial=initial_data)
    if request.method == 'POST' and form.is_valid():
        if request.user.is_authenticated:
            shipping_address = form.save(commit=False)
            shipping_address.user = request.user
            shipping_address.save()
        else:
            # Save form data to session for guest users
            request.session['guest_shipping_address'] = form.cleaned_data
        return redirect('home')
    return render(request, 'add_shipping_address.html', {'form': form})

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


