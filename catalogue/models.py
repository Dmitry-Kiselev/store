from django.db import models
from django.urls import reverse
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel
from django.utils import timezone


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

    def __str__(self):
        return self.name


class ExtraImage(models.Model):
    product = models.ForeignKey(Product, related_name='extra_images')
    image = models.ImageField(upload_to='products', blank=True, null=True)
