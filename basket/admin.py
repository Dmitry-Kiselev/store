from django.contrib import admin

from .models import Basket, Line


class LineInlineAdmin(admin.TabularInline):
    model = Line


@admin.register(Basket)
class BasketAdmin(admin.ModelAdmin):
    list_display = ['user']
    inlines = [LineInlineAdmin, ]
