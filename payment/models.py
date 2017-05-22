from django.db import models

from order.models import Order


class Payment(models.Model):
    charge_id = models.CharField(max_length=32)
    charged_sum = models.DecimalField(max_digits=10, decimal_places=2)
    discount_sum = models.DecimalField(max_digits=10, decimal_places=2)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True,
                              null=True)

    def __init__(self, *args, **kwargs):
        super(Payment, self).__init__(*args, **kwargs)

        if self.order:
            self.charged_sum = self.order.total_price
            self.discount_sum = self.order.get_discount_val
        if self.charge_id:
            self.order.status = Order.ORDER_STATUS.PROCESSING

    def __str__(self):
        return '{}'.format(self.charge_id)
