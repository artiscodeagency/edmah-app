from django.urls import path

from . import views

urlpatterns = [
    path('api/contact', views.contact_submit, name='api_contact'),
    path('api/newsletter', views.newsletter_subscribe, name='api_newsletter'),
]
