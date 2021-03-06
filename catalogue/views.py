import logging
import traceback

from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.views.generic import FormView
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from catalogue.models import Product, Category, ProductRating
from .forms import ProductRatingForm, ProductFeedbackForm

logger = logging.getLogger('django')


class IndexTemplateView(TemplateView):
    template_name = 'catalogue/index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexTemplateView, self).get_context_data()
        context['products'] = Product.objects.filter(image__isnull=False)[:6]
        context['categories'] = Category.objects.all()
        return context


class ProductListView(ListView):
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
            rating = ProductRating.objects.get(rated_product=product,
                                               user=self.request.user)
            rating = rating.rating
            context['rating_form'] = ProductRatingForm(
                initial={'rating': rating})
        except (Product.DoesNotExist, ProductRating.DoesNotExist,
                TypeError):  # TypeError for AnonymousUser
            context['rating_form'] = ProductRatingForm()
        if self.request.user.is_authenticated():
            context['feedback_form'] = ProductFeedbackForm(
                initial={'email': self.request.user.email})
        else:
            context['feedback_form'] = ProductFeedbackForm()
        return context


class FeedbackView(FormView):
    form_class = ProductFeedbackForm
    success_url = '/'
    http_method_names = ['post']

    def form_valid(self, form):
        try:
            product = Product.objects.get(pk=self.kwargs.get('pk'))
            if self.request.user.is_authenticated():
                form.instance.user = self.request.user
            form.instance.feedback_product = product
            form.instance.save()
        except Product.DoesNotExist as e:
            logger.error('{} {}: {}'.format(timezone.now(), str(e),
                                            traceback.format_exc()))
        return super(FeedbackView, self).form_valid(form)


class ProductRatingView(LoginRequiredMixin, FormView):
    form_class = ProductRatingForm
    success_url = '/'
    http_method_names = ['post']

    def form_valid(self, form):
        try:
            product = Product.objects.get(pk=self.kwargs.get('pk'))
            rating, created = ProductRating.objects.get_or_create(
                rated_product=product, user=self.request.user)
            rating.rating = form.cleaned_data['rating']
            rating.save()
        except Product.DoesNotExist as e:
            logger.error('{} {}: {}'.format(timezone.now(), str(e),
                                            traceback.format_exc()))
        return super(ProductRatingView, self).form_valid(form)
