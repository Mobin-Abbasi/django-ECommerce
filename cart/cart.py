from store.models import Product

class Cart():
    def __init__(self, request):
        self.session = request.session

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