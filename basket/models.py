from django.db import models

from catalogue.models import Product


class Basket(models.Model):
    user = models.ForeignKey('users.User')
    is_submitted = models.BooleanField(default=False)

    def __str__(self):
        return 'Baster {}'.format(self.user.username)

    @property
    def total_price(self):
        return sum([line.line_price for line in self.lines.all()])


class Line(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    basket = models.ForeignKey(Basket, on_delete=models.CASCADE,
                               related_name='lines')

    @property
    def line_price(self):
        return self.product.price * self.quantity
