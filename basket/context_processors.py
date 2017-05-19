from django.core.cache import cache
from redis.exceptions import ConnectionError


def basket_lines_count(request):
    count = None
    conn_error = False
    key = None
    if not request.user.is_authenticated():
        return {}
    try:
        key = request.user.basket.pk
        count = cache.get('basket_{}'.format(key))
    except AttributeError:
        count = None
        conn_error = True
    except ConnectionError:
        count = None
        conn_error = True
    finally:
        if count is None:
            count = request.user.basket.all_lines().count()
            if not conn_error:
                cache.set('basket_{}'.format(key), count, None)

    return {
        'basket_lines_count': count or 'empty'}
