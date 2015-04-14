from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^accounts/', include('allauth.urls')),
    url(r'^$', 'dashboard.views.dashboard', name='dashboard'),

    # sites
    url(r'^sites/$', 'tlssite.views.site_list', name='site_list'),
    url(r'^sites/add/$', 'tlssite.views.site_add_edit', name='site_add'),
    url(r'^sites/(?P<siteid>\w+)/$', 'tlssite.views.site_details', name='site_details'),
    url(r'^sites/(?P<siteid>\w+)/edit/$', 'tlssite.views.site_add_edit', name='site_edit'),
    url(r'^sites/(?P<siteid>\w+)/delete/$', 'tlssite.views.site_delete', name='site_delete'),
    url(r'^sites/(?P<siteid>\w+)/check/$', 'tlssite.views.site_check', name='site_check'),
    url(r'^sites/(?P<siteid>\w+)/nagios/$', 'tlssite.views.site_nagios', name='site_nagios'),

    # groups
    url(r'^groups/$', 'group.views.group_list', name='group_list'),
    url(r'^groups/add/$', 'group.views.group_add_edit', name='group_add'),
    url(r'^groups/(?P<groupid>\w+)/edit/$', 'group.views.group_add_edit', name='group_edit'),
    url(r'^groups/(?P<groupid>\w+)/delete/$', 'group.views.group_delete', name='group_delete'),
    url(r'^groups/(?P<groupid>\w+)/$', 'group.views.group_details', name='group_details'),
    url(r'^groups/(?P<groupid>\w+)/check/$', 'group.views.group_check', name='group_check'),

    # tags
    url(r'^tags/(?P<tagslug>[-\w\d]+)/$', 'tag.views.tag_details', name='tag_details'),
    url(r'^tags/$', 'tag.views.tag_list', name='tag_list'),
    url(r'^tags/(?P<tagslug>[-\w\d]+)/check/$', 'tag.views.tag_check', name='tag_check'),

    # alerts
    url(r'^alerts/$', 'alert.views.alert_list', name='alert_list'),
    url(r'^alerts/mine/$', 'alert.views.alert_list_user', name='alert_list_user'),
    
    url(r'^sites/(?P<siteid>\w+)/alert/$', 'alert.views.enable_site_alert', name='enable_site_alert'),
    url(r'^tags/(?P<tagslug>[-\w\d]+)/alert/$', 'alert.views.enable_tag_alert', name='enable_tag_alert'),
    url(r'^groups/(?P<groupid>\w+)/alert/$', 'alert.views.enable_group_alert', name='enable_group_alert'),
    
    url(r'^sitealerts/(?P<alertid>\w+)/disable/$', 'alert.views.disable_site_alert', name='disable_site_alert'),
    url(r'^tagalerts/(?P<alertid>\w+)/disable/$', 'alert.views.disable_tag_alert', name='disable_tag_alert'),
    url(r'^groupalerts/(?P<alertid>\w+)/disable/$', 'alert.views.disable_group_alert', name='disable_group_alert'),
)
