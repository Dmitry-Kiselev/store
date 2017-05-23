import logging
import traceback

from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.views.generic import FormView
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from catalogue.models import Product, Category, ProductRating
from conf.views import SiteInfoContextMixin
from .forms import ProductRatingForm

logger = logging.getLogger('django')


class IndexTemplateView(SiteInfoContextMixin, TemplateView):
    template_name = 'catalogue/index.html'


    def get_context_data(self, **kwargs):
        context = super(IndexTemplateView, self).get_context_data()
        context['products'] = Product.objects.filter(image__isnull=False)[:6]
        context['categories'] = Category.objects.all()
        return context


class ProductListView(SiteInfoContextMixin, ListView):
    template_name = 'catalogue/catalogue.html'
    paginate_by = 12
    context_object_name = 'products'
    model = Product

    def get_queryset(self):
        qs = super(ProductListView, self).get_queryset()
        if self.kwargs.get('category'):
            qs = qs.filter(product_category__pk=self.kwargs.get('category'))
        return qs


class ProductDetailView(DetailView):
    model = Product
    context_object_name = 'product'
    template_name = 'catalogue/product_detail.html'

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data()
        try:
            product = Product.objects.get(pk=self.kwargs.get('pk'))
            rating = ProductRating.objects.get(rated_product=product, user=self.request.user)
            rating = rating.rating
            context['rating_form'] = ProductRatingForm(initial={'rating': rating})
        except (Product.DoesNotExist, ProductRating.DoesNotExist):
            context['rating_form'] = ProductRatingForm()
        return context


class ProductRatingView(LoginRequiredMixin, FormView):
    form_class = ProductRatingForm
    success_url = '/'
    http_method_names = ['post']

    def form_valid(self, form):
        try:
            product = Product.objects.get(pk=self.kwargs.get('pk'))
            rating, created = ProductRating.objects.get_or_create(rated_product=product, user=self.request.user)
            rating.rating = form.cleaned_data['rating']
            rating.save()
        except Product.DoesNotExist as e:
            logger.error('{} {}: {}'.format(timezone.now(), str(e),
                                            traceback.format_exc()))
        return super(ProductRatingView, self).form_valid(form)
