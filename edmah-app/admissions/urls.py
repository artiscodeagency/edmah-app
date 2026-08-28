from django.urls import path

from . import views

urlpatterns = [
    path('api/register', views.submit_inscription, name='inscription_submit'),
    path('admissions/documents/', views.serve_document, name='serve_admission_document'),
]
