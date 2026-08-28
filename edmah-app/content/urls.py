from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_view, name='index'),
    path('a-propos/', views.about_view, name='about'),
    path('formations/', views.formations_view, name='formations'),
    path('cours/', views.cours_view, name='cours'),
    path('evenements/', views.evenements_view, name='evenements'),
    path('galerie/', views.gallerie_view, name='gallerie'),
    path('blog/', views.blog_view, name='blog'),
    path('blog/<slug:slug>/', views.article_detail_view, name='article_detail'),
    path('contact/', views.contact_view, name='contact'),
    path('inscriptions/', views.inscriptions_view, name='inscriptions'),
    path('certifications/', views.certifications_view, name='certifications'),
]
