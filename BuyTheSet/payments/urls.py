from django.urls import path
from . import views

urlpatterns = [
    path('process/', views.process_payment, name='process_payment'),
    path('success/', views.payment_success, name='payment_success'),
]