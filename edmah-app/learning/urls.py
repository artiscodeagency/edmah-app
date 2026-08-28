from django.urls import path

from . import views

urlpatterns = [
    path('apprenant/', views.dashboard, name='apprenant_dashboard'),
    path('apprenant/cours/<slug:slug>/', views.course_detail, name='course_detail'),
    path('apprenant/modules/<int:module_id>/quiz/', views.submit_quiz, name='submit_quiz'),
    path('apprenant/modules/<int:module_id>/notes/', views.save_note, name='save_note'),
]
