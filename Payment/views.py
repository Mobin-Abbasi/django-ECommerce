from django.shortcuts import render


# Create your views here.

def payment_success(request):
    return render(request, 'payment/payment_success.html', {})


def checkout(request):
    return render(request, 'payment/checkout.html', {})
