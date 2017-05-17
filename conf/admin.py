from django.contrib import admin
from .models import SiteConfig
from solo.admin import SingletonModelAdmin


admin.site.register(SiteConfig,SingletonModelAdmin)
