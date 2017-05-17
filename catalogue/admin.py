from django.contrib import admin
from .models import Product, Category


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'num_in_stock']


@admin.register(Category)
class CategotyAdmin(admin.ModelAdmin):
    list_display = ['name']
