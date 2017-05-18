from django.http.response import HttpResponseForbidden, HttpResponse
from django.views.generic.base import View
from extra_views import ModelFormSetView

from catalogue.models import Product
from .forms import BasketLineFormSet, LineForm
from .models import Basket, Line


class BasketAddView(View):
    def post(self, *args, **kwargs):
        basket = self.request.user.basket
        product_pk = self.request.POST.get('pk')
        if not product_pk:
            return HttpResponseForbidden()
        product = Product.objects.get(pk=product_pk)
        if basket.lines.filter(product=product).exists():
            return HttpResponseForbidden()  # product already in basket

        Line.objects.create(product=product, basket=basket)
        return HttpResponse(status=201)


class BasketView(ModelFormSetView):
    model = Line
    basket_model = Basket
    formset_class = BasketLineFormSet
    form_class = LineForm
    extra = 0
    can_delete = False
    template_name = 'basket/basket.html'

    def get_queryset(self):
        return self.request.user.basket.all_lines()
