from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.alert_list, name='alert_list'),
    path('mine/', views.alert_list_user, name='alert_list_user'),

    path('site/<int:siteid>/enable', views.enable_site_alert, name='enable_site_alert'),
    path('site/<int:siteid>/disable', views.disable_site_alert, name='disable_site_alert'),

    path('tag/<tagslug>/enable', views.enable_tag_alert, name='enable_tag_alert'),
    path('tag/<tagslug>/disable', views.disable_tag_alert, name='disable_tag_alert'),

    path('group/<int:groupid>/enable', views.enable_group_alert, name='enable_group_alert'),
    path('group/<int:groupid>/disable', views.disable_group_alert, name='disable_group_alert'),
]

