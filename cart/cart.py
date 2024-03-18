from store.models import Product, Profile


class Cart():
    def __init__(self, request):
        self.session = request.session
        # Get request
        self.request = request
        # Get the current session key if it exists
        cart = self.session.get('session_key')
        # If user is new, no session key! Create one
        if 'session_key' not in self.session:
            cart = self.session['session_key'] = {}
        # Make sure cart is available on all page of site
        self.cart = cart

    def add(self, product, quantity):
        product_id = str(product.id)
        product_qty = str(quantity)
        # Logic
        if product_id in self.cart:
            pass
        else:
            self.cart[product_id] = int(product_qty)

        self.session.modified = True
        # Deal with logged in user
        if self.request.user.is_authenticated:
            # Get the current user profile
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            # Convert {'3':1, '2':4} to {"3":1, "2":4}
            carty = str(self.cart)
            carty = carty.replace("\'", "\"")
            # Save carty to the Profile Model
            current_user.update(old_cart=str(carty))

    def __len__(self):
        return len(self.cart)

    def get_prods(self):
        # Get ids from cart
        product_ids = self.cart.keys()
        # Use ids to lookup products and database model
        products = Product.objects.filter(id__in=product_ids)
        # return those looked uo products
        return products

    def get_quants(self):
        quantities = self.cart
        return quantities

    def update(self, product, quantity):
        product_id = str(product)
        product_qty = int(quantity)
        # Get cart
        ourcart = self.cart
        # Update Dictionary
        ourcart[product_id] = product_qty
        self.session.modified = True
        thing = self.cart
        return thing

    def delete(self, product):
        product_id = str(product)
        # Delete From Dictionary/cart
        if product_id in self.cart:
            del self.cart[product_id]
        self.session.modified = True

    def cart_total(self):
        # Get product IDS
        product_ids = self.cart.keys()
        # Lookup those keys in our products database
        products = Product.objects.filter(id__in=product_ids)
        # Get quantities
        quantities = self.cart
        # Start counting with zero values
        total = 0
        for key, value in quantities.items():
            # Convert Key String into int so we can do math
            key = int(key)
            for product in products:
                if product.id == key:
                    if product.is_sale:
                        total += product.sale_price * value
                    else:
                        total += product.price * value
        return total
