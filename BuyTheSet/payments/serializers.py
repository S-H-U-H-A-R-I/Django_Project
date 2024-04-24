from .models import ShippingAddress
from store.models import Profile

class ShippingAddressSerializer:
    @staticmethod
    def get_user_shipping_address(user):
        return ShippingAddress.objects.filter(user=user).first()
    
    @staticmethod
    def get_initial_data_from_shipping_address(shipping_address):
        return {
            'full_name': shipping_address.full_name,
            'email': shipping_address.email,
            'address1': shipping_address.address1,
            'address2': shipping_address.address2,
            'phone_number': shipping_address.phone_number,
        }
    
    @staticmethod
    def get_initial_data_from_user_profile(user):
        profile = Profile.objects.filter(user=user).first()
        if profile:
            return {
                'full_name': user.get_full_name(),
                'email': profile.email,
                'phone_number': profile.phone_number,
                'address1': profile.address1,
                'address2': profile.address2,
            }
        return {}
    
    @staticmethod
    def save_shipping_address(form, user, request):
        if user.is_authenticated:
            shipping_address = form.save(commit=False)
            shipping_address.user = user
            shipping_address.save()
        else:
            request.session['guest_shipping_address'] = form.cleaned_data