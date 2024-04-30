from icecream import ic
from django.conf import settings
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.db.models import Q
from payments.models import Order, OrderItem, ShippingAddress
from .forms import SignUpForm, UpdateUserform, ChangePasswordForm, UserInfoForm
from .models import Product, Category, Profile, ProductImage


def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                email = form.cleaned_data['email']
                password = form.cleaned_data['password1']
                # Link existing shipping addresses with the same email to the new user
                shipping_addresses = ShippingAddress.objects.filter(email=email)
                if shipping_addresses.exists():
                    shipping_addresses.update(user=user)
                # Link existing orders with the same email to the new user
                orders = Order.objects.filter(email=email)
                if orders.exists():
                    orders.update(user=user)
                # login user
                user = authenticate(username=user.username, password=password)
                login(request, user)
                messages.success(request, "You have registered and logged in successfully")
                return redirect('update_info')
            except IntegrityError:
                messages.error(request, "Username already exists", "warning")
                return render(request,'register.html', {'form': form})
        else:
            messages.error(request, "Please correct the error below.", "warning")
            return render(request, 'register.html', {'form': form})
    else:  
        form = SignUpForm()    
    return render(request, 'register.html', {'form': form})


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            success_message = 'You have logged in successfully'
            alert_type ='success'
            request.session['message'] = success_message
            request.session['alert_type'] = alert_type
            return redirect('home')
        else:
            error_message = 'Username or Password is incorrect'
            alert_type = 'danger'
            context = {
                'message': error_message,
                'alert_type': alert_type
            }
            return render(request, 'login.html', context)
    else:
        return render(request, 'login.html')


def update_info(request):
    if request.user.is_authenticated:
        current_user = Profile.objects.get(user__id=request.user.id)
        form = UserInfoForm(request.POST or None, instance=current_user)
        if request.method == 'POST':
            if form.is_valid():
                form.save()
                messages.success(request, "Your information has been updated successfully.", "success")
                return redirect('update_info')
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error[0], "danger")
                return redirect('update_info')
        else:
            return render(request, 'update_info.html', {'form': form})
    else:
        messages.error(request, "You are not logged in.", "danger")
        return redirect('login')
            

def update_password(request):
    if request.user.is_authenticated:
        current_user = request.user
        if request.method == 'POST':
            form = ChangePasswordForm(current_user, request.POST)
            if form.is_valid():
                user = form.save()
                update_session_auth_hash(request, user)
                messages.success(request, "Your password has been updated successfully.", "success")
                return redirect('home')
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error[0], "danger")
                return redirect('update_password')
        else:
            form = ChangePasswordForm(current_user)
            context = {'form': form}
            return render(request, "update_password.html", context)       
    else:
        messages.error(request, "You must be logged in to update your password.", "danger")
        return redirect('login')        


def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        if request.method == 'POST':
            user_form = UpdateUserform(request.POST or None, instance=current_user)
            if user_form.is_valid():
                user_form.save()
                login(request, current_user)
                messages.success(request, "Your profile has been updated successfully.")
                return redirect('home')
            else:
                messages.error(request, "Please correct the error below.", "warning")
        else:
            user_form = UpdateUserform(instance=current_user)
            context = {
                "user_form": user_form
            }
            return render(request, "update_user.html", context)
    else:
        messages.error(request, "You must be logged in to update your profile.")
        return redirect('login')
    
    
def order_history(request):
    if not request.user.is_authenticated:
        messages.error(request, "You must be logged in to view your order history.", "danger")
        return redirect('home')
    orders = Order.objects.filter(user=request.user).order_by("-date_ordered")
    context = {
        "orders": orders
    }
    return render(request, "order_history.html", context)


def order_details(request, order_id):
    if not request.user.is_authenticated:
        messages.error(request, "You must be logged in to view your order.")
        return redirect('home')
    order = get_object_or_404(Order, id=order_id, user=request.user)
    context = {
        "order": order,
    }
    return render(request, "order_details.html", context)
    
    
def category_summary(request):
    categories = Category.objects.all()
    context = {
        "categories": categories
    }
    return render(request, "category_summary.html", context)


def category(request, foo):
    # Replace hyphens with spaces
    foo = foo.replace('-', ' ')
    # Grab the category from the url
    try:
        # Look for the category
        category = Category.objects.get(name=foo)
        products = Product.objects.filter(category=category, quantity__gt=0).order_by("-sale_price", "name")
        context = {
            "products": products,
            "category": category,
        }
        return render (request, "category.html", context)
    except Category.DoesNotExist:
        messages.error(request, f"Category '{foo}' does not exist.", "warning")
        return redirect('home')
    

def product(request, pk):
    product = get_object_or_404(Product, id=pk)
    additional_images = ProductImage.objects.filter(product=product)
    images  = [product.image.url] + [f"{settings.MEDIA_URL}{image}" for image in additional_images.values_list('image', flat=True)]
    context = {
        "product": product,
        "images": images,
    }
    return render(request, 'product.html', context)


def home(request):
    products = Product.objects.filter(quantity__gt=0).order_by('-is_sale')
    message = request.session.pop('message', None)
    alert_type = request.session.pop('alert_type', None)
    context = {
        'products': products,
        'message': message,
        'alert_type': alert_type
    }
    return render(request, 'home.html', context)


def about(request):
    return render(request, 'about.html')


def logout_user(request):
    logout(request)
    success_message = "You have been logged out successfully."
    alert_type = "success"
    request.session['message'] = success_message
    request.session['alert_type'] = alert_type
    return redirect('home')


def product_search(request):
    query = request.GET.get('q', '')
    category_name = request.GET.get('category', None)
    if category_name:
        category = Category.objects.filter(name=category_name).first()
        if category:
            products = Product.objects.filter(Q(name__icontains=query) | Q(description__icontains=query), category=category).order_by('-is_sale').distinct()
        else:
            products = []
    else:
        products = Product.objects.filter(Q(name__icontains=query) | Q(description__icontains=query)).order_by('-is_sale').distinct()
    context = {
        'products': products,
        'query': query,
        'category': category_name,
    }
    return render(request, 'search_results.html', context)
    