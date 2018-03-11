from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.site_list, name='site_list'),
    path('add/', views.site_add_edit, name='site_add'),
    path(
        '<int:siteid>/', include([
            path('', views.site_details, name='site_details'),
            path('edit/', views.site_add_edit, name='site_edit'),
            path('delete/', views.site_delete, name='site_delete'),
            path('check/', views.site_check, name='site_check'),
            path('nagios/', views.site_nagios, name='site_nagios')
        ])
    )
]

