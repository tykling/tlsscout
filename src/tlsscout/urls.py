from django.contrib import admin
from django.urls import path, include
from dashboard.views import dashboard

urlpatterns = [
    # admin site
    path('admin/', admin.site.urls),

    # frontpage
    path('', dashboard, name='dashboard'),

    path('accounts/', include('allauth.urls')),
    path('sites/', include('tlssite.urls')),
    path('groups/', include('group.urls')),
    path('tags/', include('tag.urls')),
    path('alerts/', include('alert.urls')),
    path('events/', include('eventlog.urls')),
    path('metrics/', include('metrics.urls')),
]

