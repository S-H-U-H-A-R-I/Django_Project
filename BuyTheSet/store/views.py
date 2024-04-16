from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ObjectDoesNotExist
from .forms import SignUpForm
from .models import Product, Category


def category(request, foo):
    # Replace Spaces with Hyphens
    foo = foo.replace('-', ' ')
    # Grab the category from the url
    try:
        # Look for the category
        category = Category.objects.get(name=foo)
        products = Product.objects.filter(category=category).order_by("-sale_price", "name")
        context = {
            "products": products,
            "category": category,
        }
        return render (request, "category.html", context)
    except ObjectDoesNotExist:
        messages.error(request, f"Category '{foo}' does not exist.", "warning")
        return redirect('home')
    


def product(request, pk):
    product = Product.objects.get(id=pk)
    return render(request, 'product.html', {'product': product})


def home(request):
    products = Product.objects.all().order_by('-is_sale')
    context = {
        'products': products
    }
    return render(request, 'home.html', context)


def about(request):
    return render(request, 'about.html')


def login_user(request):
    if request.method == 'POST':
        usermname = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=usermname, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"You have successfully logged in as {user.username}")
            return redirect('home')
        else:
            messages.error(request,  'Username or Password is incorrect', "danger")
            return redirect('login')
    else:
        return render(request, 'login.html', )


def logout_user(request):
    logout(request)
    messages.success(request, "You have successfully logged out.")
    return redirect('home')


def register_user(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if  form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            # login user
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "You have registered and logged in successfully")
            return redirect('home')
        else:
            messages.error(request, "Please correct the error below.", "warning")
            return render(request, 'register.html', {'form': form})
    else:      
        return render(request, 'register.html', {'form': form})
    