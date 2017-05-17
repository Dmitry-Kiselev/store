from django.contrib import admin
from .models import Product, Category, ExtraImage


class ExtraImageAdmin(admin.TabularInline):
    model = ExtraImage
    extra = 0


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'num_in_stock']
    inlines = [ExtraImageAdmin, ]


@admin.register(Category)
class CategotyAdmin(admin.ModelAdmin):
    list_display = ['name']
