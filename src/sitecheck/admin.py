from django.contrib import admin
from . import models

admin.site.register(models.SiteCheck)
admin.site.register(models.SiteCheckResult)

