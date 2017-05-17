from django.views.generic.base import ContextMixin

from conf.models import SiteConfig


class SiteInfoContextMixin(ContextMixin):
    def get_context_data(self, **kwargs):
        context = super(SiteInfoContextMixin, self).get_context_data()
        conf = SiteConfig.get_solo()
        context['company_name'] = conf.company_name
        return context
