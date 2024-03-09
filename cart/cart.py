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
        