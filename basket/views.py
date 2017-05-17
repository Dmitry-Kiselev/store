from django.views.generic.base import View
from .models import Basket, Line
from django.http.response import HttpResponseForbidden, HttpResponse
from catalogue.models import Product


class BasketAddView(View):
    def post(self, *args, **kwargs):
        basket, created = Basket.objects.get_or_create(user=self.request.user,
                                              is_submitted=False)
        product_pk = self.request.POST.get('pk')
        if not product_pk:
            return HttpResponseForbidden()
        product = Product.objects.get(pk=product_pk)
        if basket.lines.filter(product=product).exists():
            return HttpResponseForbidden()  # product already in basket

        Line.objects.create(product=product, basket=basket)
        return HttpResponse(status=201)
