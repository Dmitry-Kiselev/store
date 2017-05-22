from django.core.cache import cache
from redis.exceptions import ConnectionError


def basket_lines_count(request):
    if not request.user.is_authenticated():
        return {}
    try:
        key = request.user.basket.pk
        count = cache.get('basket_{}'.format(key))
    except (AttributeError, ConnectionError):
        count = request.user.basket.all_lines().count()
    else:
        cache.set('basket_{}'.format(key), count, None)

    return {
        'basket_lines_count': count or 'empty'}
