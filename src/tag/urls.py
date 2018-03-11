from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.tag_list, name='tag_list'),
    path(
        '<tagslug>/', include([
            path('', views.tag_details, name='tag_details'),
            path('check/', views.tag_check, name='tag_check'),
        ])
    )
]

