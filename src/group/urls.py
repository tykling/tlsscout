from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.group_list, name='group_list'),
    path('add/', views.group_add_edit, name='group_add'),
    path(
        '<int:groupid>/', include([
            path('', views.group_details, name='group_details'),
            path('edit/', views.group_add_edit, name='group_edit'),
            path('delete/', views.group_delete, name='group_delete'),
            path('check/', views.group_check, name='group_check'),
        ])
    )
]

