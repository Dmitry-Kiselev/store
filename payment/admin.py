from django.contrib import admin

from payment.models import StripePayment


@admin.register(StripePayment)
class StripePaymentAdmin(admin.ModelAdmin):
    list_display = ['charge_id', 'charged_sum', ]
