from django.contrib import admin
from . import models

admin.site.register(models.SiteAlert)
admin.site.register(models.TagAlert)
admin.site.register(models.GroupAlert)
admin.site.register(models.AlertHistory)

