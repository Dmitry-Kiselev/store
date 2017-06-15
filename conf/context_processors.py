from conf.models import SiteConfig


def general_site_info_processor(request):
    conf = SiteConfig.get_solo()
    return {
        'company_name': conf.company_name
    }
