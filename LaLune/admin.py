from django.contrib import admin
from .models import Profile
from .models import Product
from .models import Order
from .models import OrderItem
from .models import ShippingAddress



admin.site.register(Profile)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)

