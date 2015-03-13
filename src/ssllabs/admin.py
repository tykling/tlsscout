from django.contrib import admin
from ssllabs.models import ApiClientState, RequestLog

admin.site.register(ApiClientState)
admin.site.register(RequestLog)