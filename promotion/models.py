from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from catalogue.models import TimeStampedModel
from .tasks import send_promo


class PromotionLetter(TimeStampedModel):
    promo_subject = models.CharField(max_length=120)
    promo_text = models.TextField()
    start_at = models.DateTimeField()


@receiver(post_save, sender=PromotionLetter)
def send_email_to_customer(sender, instance, created, **kwargs):
    if created:
        send_promo.apply_async((instance.pk,), eta=instance.start_at)
