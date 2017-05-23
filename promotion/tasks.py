from __future__ import absolute_import, unicode_literals

from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from users.models import User


@shared_task
def send_promo(promo_pk):
    from .models import PromotionLetter  # to avoid circular import

    try:
        letter = PromotionLetter.objects.get(pk=promo_pk)
        emails = User.objects.all().values_list('email', flat=True)[::1]
    except PromotionLetter.DoesNotExist:
        return
    send_mail(
        letter.promo_subject,
        letter.promo_text,
        settings.DEFAULT_FROM_EMAIL,
        [emails],
    )
