from django.conf import settings
from django.db import models
from django.db.models import Avg
from django.urls import reverse
from django.utils import timezone
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)


class Category(MPTTModel, TimeStampedModel):
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    name = models.CharField(max_length=50, unique=True)
    parent = TreeForeignKey('self', null=True, blank=True,
                            related_name='children', db_index=True)
    image = models.ImageField(upload_to='categories', blank=True, null=True)

    def get_absolute_url(self):
        return reverse('catalogue', kwargs={'category': self.pk})

    def __str__(self):
        return self.name


class Product(TimeStampedModel):
    name = models.CharField(max_length=50, unique=True)
    product_category = models.ForeignKey(Category, on_delete=models.SET_NULL,
                                         blank=True, null=True,
                                         related_name='products')
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    num_in_stock = models.IntegerField()
    image = models.ImageField(upload_to='products', blank=True, null=True)

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'pk': self.pk})

    @property
    def rating(self):
        return list(ProductRating.objects.filter(rated_product=self).aggregate(
            Avg('rating')).values())[0]

    def __str__(self):
        return self.name


class ExtraImage(models.Model):
    product = models.ForeignKey(Product, related_name='extra_images')
    image = models.ImageField(upload_to='products', blank=True, null=True)


class ProductRating(TimeStampedModel):
    rated_product = models.ForeignKey(Product, related_name='ratings',
                                      null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True)
    rating = models.PositiveSmallIntegerField(null=True, default=5)


class ProductFeedback(TimeStampedModel):
    class FEEDBACK_STATUS:
        NEW = 0
        PROCESSING = 1
        INVALID = 2
        COMPLETED = 3

        FEEDBACK_CHOICES = (
            (NEW, 'New'),
            (PROCESSING, 'Processing'),
            (INVALID, 'Invalid'),
            (COMPLETED, 'Completed')
        )

    feedback_product = models.ForeignKey(Product, related_name='feedback',
                                null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True,
                             related_name='feedback')
    feedback = models.TextField()
    email = models.EmailField(blank=True, null=True)
    status = models.SmallIntegerField(choices=FEEDBACK_STATUS.FEEDBACK_CHOICES,
                                      default=FEEDBACK_STATUS.NEW)
    answer = models.TextField()
    answered_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True,
                                    blank=True, related_name='feedback_answers')
