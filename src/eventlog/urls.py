from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.event_list, name='event_list'),
]

