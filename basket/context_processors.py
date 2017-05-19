from django.core.cache import cache
from redis.exceptions import ConnectionError


def basket_lines_count(request):
    count = None
    try:
        key = request.user.basket.pk
        count = cache.get('basket_%s' % key)
    except AttributeError:
        count = None
    except ConnectionError:
        count = None
    finally:
        if count is None:
            count = request.user.basket.all_lines().count()

    return {
        'basket_lines_count': count or 'empty'}
