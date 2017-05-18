from django.contrib import admin

from .models import Order, Payment, Discount


admin.site.register(Payment)
admin.site.register(Order)
admin.site.register(Discount)
