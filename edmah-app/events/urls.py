from django.urls import path

from . import views

urlpatterns = [
    path('evenements/<slug:slug>/inscription/', views.register_for_event, name='event_register'),
]
