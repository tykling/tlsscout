from django.contrib import admin
from sitecheck.models import SiteCheck, SiteCheckResult

admin.site.register(SiteCheck)
admin.site.register(SiteCheckResult)
