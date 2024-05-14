from django.contrib import admin
from .models import *
from django.contrib.auth.models import User

# Register your models here.


# Register the model on the admin section thing
admin.site.register(ShippingAddress)
admin.site.register(Order)
admin.site.register(OrderItem)


# Create an OrderItems Inline
class OrderItemInline(admin.StackedInline):
    model = OrderItem
    extra = 0


# Extend ore Order Model
class OrderAdmin(admin.ModelAdmin):
    model = Order
    readonly_fields = ["date_ordered"]
    fields = ["user", "full_name", "email", "shipping_address", "amount_paid", "date_ordered"]
    inlines = [OrderItemInline]


# Unregister Order Model
admin.site.unregister(Order)

# Re-Register our Order AND OrderAdmin
admin.site.register(Order, OrderAdmin)