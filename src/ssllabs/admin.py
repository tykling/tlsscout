from django.contrib import admin
from . import models

admin.site.register(models.ApiClientState)

class RequestLogAdmin(admin.ModelAdmin):
    readonly_fields = ['sitecheck']

admin.site.register(models.RequestLog, RequestLogAdmin)

