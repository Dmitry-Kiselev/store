from django.contrib import admin

from .models import Product, Category, ExtraImage, ProductRating, \
    ProductFeedback


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


@admin.register(ProductRating)
class ProductRatingAdmin(admin.ModelAdmin):
    list_display = ['created_at', 'updated_at', 'rating']


@admin.register(ProductFeedback)
class ProductFeedbackAdmin(admin.ModelAdmin):
    list_display = ['created_at', 'updated_at', 'status']
    readonly_fields = ('answered_by',)

    def save_model(self, request, obj, form, change):
        obj.answered_by = request.user
        obj.save()
