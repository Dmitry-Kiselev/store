import logging
import traceback

from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone

from conf.models import SiteConfig


class BaseMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response


class AdminNotifyMiddleware(BaseMiddleware):
    def process_exception(self, request, exception):
        conf = SiteConfig.get_solo()
        mail_to = conf.admin_email
        if not mail_to:
            return
        subject = str(exception)
        message = traceback.format_exc()
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [mail_to, ])


class LoggingMiddleware(BaseMiddleware):
    def process_exception(self, request, exception):
        logger = logging.getLogger(__name__)
        logger.error('{} {}: {}'.format(timezone.now(), str(exception),
                                        traceback.format_exc()))
