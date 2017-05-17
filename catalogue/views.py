from django.views.generic.base import TemplateView

from catalogue.models import Product, Category
from conf.views import SiteInfoContextMixin


class IndexTemplateView(SiteInfoContextMixin, TemplateView):
    template_name = 'catalogue/index.html'


    def get_context_data(self, **kwargs):
        context = super(IndexTemplateView, self).get_context_data()
        context['products'] = Product.objects.filter(image__isnull=False)[:6]
        context['categories'] = Category.objects.all()
        return context