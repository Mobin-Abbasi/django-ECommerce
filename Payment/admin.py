from django.contrib import admin
from .models import *

# Register your models here.


# Register the model on the admin section thing
admin.site.register(ShippingAddress)
admin.site.register(Order)
admin.site.register(OrderItem)

