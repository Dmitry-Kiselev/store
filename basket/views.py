from django.http.response import HttpResponseForbidden
from django.views.generic.base import View
from extra_views import ModelFormSetView

from catalogue.models import Product
from .forms import BasketLineFormSet, LineForm
from .models import Basket, Line
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin



class BasketAddView(LoginRequiredMixin, View):
    def post(self, *args, **kwargs):
        basket = self.request.user.basket
        product_pk = self.request.POST.get('pk')
        if not product_pk:
            return HttpResponseForbidden()
        product = Product.objects.get(pk=product_pk)
        if basket.lines.filter(product=product).exists():
            return redirect('catalogue')  # product already in basket

        Line.objects.create(product=product, basket=basket)
        return redirect('catalogue')


class BasketView(LoginRequiredMixin, ModelFormSetView):
    model = Line
    basket_model = Basket
    formset_class = BasketLineFormSet
    form_class = LineForm
    extra = 0
    can_delete = True
    template_name = 'basket/basket.html'


    def get_queryset(self):
        return self.request.user.basket.all_lines()
