import logging
import traceback

from django.core.cache import cache
from django.utils import timezone
from redis.exceptions import ConnectionError


def basket_lines_count(request):
    if not request.user.is_authenticated():
        return {}
    try:
        key = request.user.basket.pk
        count = cache.get('basket_{}'.format(key))
    except (AttributeError, ConnectionError):
        count = request.user.basket.all_lines().count()
        logger = logging.getLogger(__name__)
        logger.error('{} {}: {}'.format(timezone.now(), str(e),
                                        traceback.format_exc()))

    else:
        cache.set('basket_{}'.format(key), count, None)

    return {
        'basket_lines_count': count or 'empty'}
