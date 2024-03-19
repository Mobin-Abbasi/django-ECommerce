from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class ShippingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shipping_address', null=True, blank=True)
    full_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    address1 = models.CharField(max_length=255)
    address2 = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255, null=True, blank=True)
    zipcode = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(max_length=255)

    # Don't pluralize address
    class Meta:
        verbose_name_plural = 'Shipping Addresses'

    def __str__(self):
        return f'Shipping Address - {str(self.id)}'
