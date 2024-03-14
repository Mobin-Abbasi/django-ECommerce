from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .forms import *
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
            messages.success(request, 'You have been registered and logged in!!! Welcome!!')
            return redirect('store:home')
        else:
            messages.error(request, 'Invalid username or password')
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
