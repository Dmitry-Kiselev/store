from django.core.cache import cache

def basket_lines_count(request):
    try:
        key = request.user.basket.pk
        count = cache.get('basket_%s' % key)
        if count is None:
            count = request.user.basket.all_lines().count()
    except AttributeError:
        count = None
    return {
        'basket_lines_count': count or 'empty'}
