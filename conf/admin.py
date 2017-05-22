from django.contrib import admin
from solo.admin import SingletonModelAdmin

from .models import SiteConfig

admin.site.register(SiteConfig,SingletonModelAdmin)
