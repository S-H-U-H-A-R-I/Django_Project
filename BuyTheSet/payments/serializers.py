from .forms import ShippingAddressForm
from .models import ShippingAddress
from store.models import Profile
from cart.serializers import CartSerializer


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
            shipping_address = ShippingAddressSerializer.get_user_shipping_address(user)
            if shipping_address:
                form = ShippingAddressForm(request.POST, instance=shipping_address)
                form.save()
            else:
                shipping_address = form.save(commit=False)
                shipping_address.user = user
                shipping_address.save()
        else:
            shipping_address = form.save(commit=False)
            shipping_address.save()
            request.session['guest_shipping_address_id'] = shipping_address.id
            
            
class PaymentSerializer:
    @staticmethod
    def get_cart_items_data(cart):
        cart_items = CartSerializer.get_cart_items(cart)
        cart_items_data = []
        for item in cart_items:
            item_data = {
                'name': item.product.name,
                'price': item.product.sale_price if item.product.is_sale else item.product.price,
                'quantity': item.quantity,
                'total': item.product.sale_price * item.quantity if item.product.is_sale else item.product.price * item.quantity,
            }
            cart_items_data.append(item_data)
        return cart_items_data
    
    @staticmethod
    def get_cart_total(cart):
        return CartSerializer.get_cart_total(cart)


