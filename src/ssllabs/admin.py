from django.contrib import admin
from . import models

admin.site.register(models.ApiClientState)
admin.site.register(models.RequestLog)

