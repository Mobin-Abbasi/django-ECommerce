from django.shortcuts import render
from .models import *

# Create your views here.


def home(request):
    products = Product.objects.all()
    context = {
        'products': products
    }
    return render(request, 'home.html', context)
