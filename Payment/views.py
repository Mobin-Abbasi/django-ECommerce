from django.contrib import messages
from django.shortcuts import render, redirect
from cart.cart import Cart
from .forms import ShippingForm, PaymentForm
from .models import *
from django.contrib.auth.models import User
from store.models import Profile, Product


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
        # Create Session with Shipping info
        my_shipping = request.POST
        request.session['my_shipping'] = my_shipping
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


def process_order(request):
    if request.POST:
        # Get the cart
        cart = Cart(request)
        cart_products = cart.get_prods
        quantities = cart.get_quants
        totals = cart.cart_total()
        # Get Billing Information from the last page
        payment_form = PaymentForm(request.POST or None)
        # Get Shipping Session Data
        my_shipping = request.session.get('my_shipping')
        # Gather Order Info
        full_name = my_shipping['shipping_full_name']
        email = my_shipping['shipping_email']
        # Create Shipping Address from Session info
        shipping_address = (f"{my_shipping['shipping_address1']}\n{my_shipping['shipping_address2']}\n"
                            f"{my_shipping['shipping_city']}\n{my_shipping['shipping_state']}\n"
                            f"{my_shipping['shipping_zipcode']}\n{my_shipping['shipping_country']}")
        amount_paid = totals
        # Create an Order
        if request.user.is_authenticated:
            # logged in
            user = request.user
            # Create Order
            creat_order = Order(user=user, email=email, full_name=full_name, amount_paid=amount_paid,
                                shipping_address=shipping_address)
            creat_order.save()
            # Add Order Items
            # Get The Order ID
            order_id = creat_order.pk
            # Get Product Info
            for product in cart_products():
                # Get Product ID
                product_id = product.id
                # Get Product Price
                if product.is_sale:
                    price = product.sale_price
                else:
                    price = product.price
                # Get Quantity
                for key, value in quantities().items():
                    if int(key) == product.id:
                        # Create Order Item
                        creat_order_item = OrderItem(order_id=order_id, product_id=product_id,
                                                     user=user, quantity=value, price=price, )
                        creat_order_item.save()

            # Delete our cart
            for key in list(request.session.keys()):
                if key == "session_key":
                    # Delete The Key
                    del request.session[key]

            messages.success(request, 'Order Placed!')
            return redirect('store:home')
        else:
            # not logged in
            creat_order = Order(email=email, full_name=full_name, amount_paid=amount_paid,
                                shipping_address=shipping_address)
            creat_order.save()
            # Add Order Items
            # Get The Order ID
            order_id = creat_order.pk
            # Get Product Info
            for product in cart_products():
                # Get Product ID
                product_id = product.id
                # Get Product Price
                if product.is_sale:
                    price = product.sale_price
                else:
                    price = product.price
                # Get Quantity
                for key, value in quantities().items():
                    if int(key) == product.id:
                        # Create Order Item
                        creat_order_item = OrderItem(order_id=order_id, product_id=product_id, quantity=value,
                                                     price=price, )
                        creat_order_item.save()

            # Delete our cart
            for key in list(request.session.keys()):
                if key == "session_key":
                    # Delete The Key
                    del request.session[key]

            # Delete cart from database (old_cart field)
            current_user = Profile.objects.filter(user__id=request.user.id)
            # Delete shopping cart in database (old_cart field)
            current_user.update(old_cart='')

            messages.success(request, 'Order Placed!')
            return redirect('store:home')

    else:
        messages.success(request, 'Access Denied')
        return redirect('store:home')


def shipped_dash(request):
    if request.user.is_authenticated and request.user.is_superuser:
        orders = Order.objects.filter(shipped=True)

        if request.POST:
            status = request.POST["shipping_status"]
            num = request.POST["num"]
            # grab the order
            order = Order.objects.filter(id=num)
            # update the order
            order.update(shipped=False)
            messages.success(request, 'Shipping Status Updated')
            return redirect('store:home')

        context = {
            'orders': orders,
        }
        return render(request, 'payment/shipped_dash.html', context)
    else:
        messages.success(request, 'Access Denied')
        return redirect('store:home')


def not_shipped_dash(request):
    if request.user.is_authenticated and request.user.is_superuser:
        orders = Order.objects.filter(shipped=False)

        if request.POST:
            status = request.POST["shipping_status"]
            num = request.POST["num"]
            # grab the order
            order = Order.objects.filter(id=num)
            # update the order
            order.update(shipped=True)
            messages.success(request, 'Shipping Status Updated')
            return redirect('store:home')

        context = {
            'orders': orders,
        }
        return render(request, 'payment/not_shipped_dash.html', context)
    else:
        messages.success(request, 'Access Denied')
        return redirect('store:home')


def orders(request, pk):
    if request.user.is_authenticated and request.user.is_superuser:
        # Get the order
        order = Order.objects.get(id=pk)
        # Get the order items
        items = OrderItem.objects.filter(order=pk)

        if request.POST:
            status = request.POST["shipping_status"]
            # Check if true or false
            if status == 'true':
                # Get the order
                order = Order.objects.filter(id=pk)
                # Update The Status
                order.update(shipped=True)
            else:
                # Get the order
                order = Order.objects.filter(id=pk)
                # Update The Status
                order.update(shipped=False)
            messages.success(request, 'Shipping Status Updated')
            return redirect('store:home')

        context = {
            "order": order,
            "items": items,
        }
        return render(request, 'payment/orders.html', context)
    else:
        messages.success(request, 'Access Denied')
        return redirect('store:home')