from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from catalogue.models import Product, Category
from conf.views import SiteInfoContextMixin


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
