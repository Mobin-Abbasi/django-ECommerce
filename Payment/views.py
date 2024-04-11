from django.contrib import messages
from django.shortcuts import render, redirect
from cart.cart import Cart
from .forms import ShippingForm, PaymentForm
from .models import ShippingAddress


# Create your views here.

def payment_success(request):
    return render(request, "payment/payment_success.html", {})


def checkout(request):
    # Get the cart
    cart = Cart(request)
    cart_products = cart.get_prods
    quantities = cart.get_quants
    totals = cart.cart_total()
    if request.user.is_authenticated:
        # Checkout as logged in user
        # Shipping User
        # shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
        # Sipping Form
        shipping_form = ShippingForm(request.POST)
        context = {
            'cart_products': cart_products,
            'quantities': quantities,
            'totals': totals,
            'shipping_form': shipping_form,
        }
        return render(request, "payment/checkout.html", context)
    else:
        # Checkout as guest
        shipping_form = ShippingForm(request.POST or None)
        context = {
            'cart_products': cart_products,
            'quantities': quantities,
            'totals': totals,
            'shipping_form': shipping_form,
        }
        return render(request, 'payment/checkout.html', context)


def billing_info(request):
    if request.method == 'POST':
        # Get the cart
        cart = Cart(request)
        cart_products = cart.get_prods
        quantities = cart.get_quants
        totals = cart.cart_total()
        # Check to See if user is Logged in
        if request.user.is_authenticated:
            # Get The Billing Form
            billing_form = PaymentForm()
            context = {
                'cart_products': cart_products,
                'quantities': quantities,
                'totals': totals,
                'shipping_info': request.POST,
                'billing_form': billing_form,
            }
            return render(request, 'payment/billing_info.html', context)
        else:
            # Not Logged in
            # Get The Billing Form
            billing_form = PaymentForm()
            pass
        context = {
            'cart_products': cart_products,
            'quantities': quantities,
            'totals': totals,
            'shipping_info': request.POST,
            'billing_form': billing_form,
        }
        return render(request, 'payment/billing_info.html', context)
    else:
        messages.success(request, 'Access Denied')
        return redirect('store:home')
