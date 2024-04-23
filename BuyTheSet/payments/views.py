from django.shortcuts import render, redirect
from .forms import PaymentForm

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


