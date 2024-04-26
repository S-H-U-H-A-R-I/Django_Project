from django.urls import path
from . import views

urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path('save-shipping-info/', views.save_shipping_info, name='save_shipping_info'),
    path('success/', views.payment_success, name='payment_success'),
]