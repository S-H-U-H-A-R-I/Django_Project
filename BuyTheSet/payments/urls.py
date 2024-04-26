from django.urls import path
from . import views

urlpatterns = [
    path('shipping_address/', views.add_shipping_address, name='shipping_address'),
    path('checkout/', views.checkout, name='checkout'),
    path('process/', views.process_payment, name='process_payment'),
    path('success/', views.payment_success, name='payment_success'),
]