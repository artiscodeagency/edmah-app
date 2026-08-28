from django.urls import path

from . import views

urlpatterns = [
    path('api/certificates/verify', views.verify_certificate, name='verify_certificate'),
]
