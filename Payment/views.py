from django.shortcuts import render
from cart.cart import Cart
from .forms import ShippingForm
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
        shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
        # Sipping Form
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)
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
    pass
