from __future__ import absolute_import, unicode_literals

from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail


@shared_task
def send_email(email=None):
    if email:
        send_mail(
            'Thanks for your order!',
            'We will contact you as soon as possible.',
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
        )
