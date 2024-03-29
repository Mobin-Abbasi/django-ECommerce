from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .forms import *
from django.db.models import Q
import json
from cart.cart import Cart
from Payment.forms import ShippingForm
from Payment.models import ShippingAddress


# Create your views here.


def home(request):
    products = Product.objects.all()
    context = {
        'products': products
    }
    return render(request, 'home.html', context)


def product_detail(request, pk):
    product = Product.objects.get(pk=pk)
    context = {
        'product': product
    }
    return render(request, 'product.html', context)


def about(request):
    return render(request, 'about.html', {})


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Do Some Shopping Cart Stuff
            current_user = Profile.objects.get(user__id=request.user.id)
            # Get their saved cart from database
            saved_cart = current_user.old_cart
            # Convert Database String to Python dictionary
            if saved_cart:
                # Convert to dictionary using JSON
                converted_cart = json.loads(saved_cart)
                # Add the loaded cart dictionary to our session
                # Get the cart
                cart = Cart(request)
                # Loop Thru the cart and add the items from the database
                for key, value in converted_cart.items():
                    cart.db_add(product=key, quantity=value)

            messages.success(request, 'You have been logged in')
            return redirect('store:home')
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('store:login')
    else:
        return render(request, 'login.html', {})


def logout_user(request):
    logout(request)
    messages.success(request, 'You have been logged out')
    return redirect('store:home')


def register_user(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            # log in user
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "Username Created - Please Fill Out Your User Info Below...")
            return redirect('store:update_info')
        else:
            messages.error(request, 'Whoops! There was a problem Registering, please try again...')
            return redirect('store:register')
    else:
        return render(request, 'register.html', {'form': form})


def category(request, foo):
    # Replace Hyphens with spaces
    foo = foo.replace('-', ' ')
    # Grab the category from url
    try:
        # Look up the Category
        category = Category.objects.get(name=foo)
        products = Product.objects.filter(category=category)
        context = {
            'category': category,
            'products': products,
        }
        return render(request, 'category.html', context)
    except:
        messages.success(request, "That category Doesn't Exist...")
        return redirect('store:home')


def category_summary(request):
    categories = Category.objects.all()
    context = {
        'categories': categories
    }
    return render(request, 'category_summary.html', context)


def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        user_form = UpdateUserForm(request.POST or None, instance=current_user)
        if user_form.is_valid():
            user_form.save()
            login(request, current_user)
            messages.success(request, 'User has been updated!!!')
            return redirect('store:home')
        context = {
            'current_user': current_user,
            'user_form': user_form,
        }
        return render(request, 'update_user.html', context)
    else:
        messages.success(request, 'You Must Be Logged in To Access That Page!!!')
        return redirect('store:home')


def update_password(request):
    if request.user.is_authenticated:
        current_user = request.user
        # Did they fill out the form
        if request.method == 'POST':
            form = ChangePasswordForm(current_user, request.POST)
            # Is The Form Valid
            if form.is_valid():
                form.save()
                messages.success(request, 'Your password has been updated, Please Login Again...')
                login(request, current_user)
                return redirect('store:update_user')
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)
                    return redirect('store:update_password')
        else:
            form = ChangePasswordForm(current_user)
            context = {
                'form': form
            }
            return render(request, 'update_password.html', context)
    else:
        messages.success(request, 'You Must Be Logged In To View That Page...')
        return redirect('store:home')


def update_info(request):
    if request.user.is_authenticated:
        # Get Current User
        current_user = Profile.objects.get(user__id=request.user.id)
        # Get Current User's Shipping Info
        shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
        # Get original User Form
        form = UserInfoForm(request.POST or None, instance=current_user)
        # Get User's Shipping Form
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)
        if form.is_valid() or shipping_form.is_valid():
            # Save original form
            form.save()
            # Save shipping form
            shipping_form.save()
            messages.success(request, "Your Info Has Been Updated!!")
            return redirect('home')
        context = {
            'form': form,
            'shipping_form': shipping_form,
        }
        return render(request, "update_info.html", context)
    else:
        messages.success(request, "You Must Be Logged In To Access That Page!!")
        return redirect('store:home')


def search(request):
    # Determine of they filled out the form
    if request.method == 'POST':
        searched = request.POST['searched']
        # Query the products DB model
        searched = Product.objects.filter(Q(name__icontains=searched) | Q(description__icontains=searched))
        # Test For null
        if not searched:
            messages.error(request, 'That Products Does not Exist...Please Try Again!!')
            return render(request, 'search.html', {})
        else:
            return render(request, 'search.html', {'searched': searched})
    else:
        return render(request, 'search.html', {})
