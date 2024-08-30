from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

app_name = 'centres'

urlpatterns = [
    # Routes pour la page d'accueil
    path('', views.home, name='home'),

    # Routes pour les Centres de Formation
    path('centres/', views.centre_list, name='centre_list'),
    path('centre/<int:pk>/', views.centre_detail, name='centre_detail'),

    # Routes pour les Personnes
    path('personne/ajouter/', views.personne_create, name='personne_create'),

    # Routes pour les Formations
    path('formations/', views.formation_list, name='formation_list'),
    path('formation/<int:pk>/', views.formation_detail, name='formation_detail'),
    path('formation/ajouter/', views.formation_create, name='formation_create'),

    # Routes pour les Sessions de Formation
    path('sessions/', views.session_list, name='session_list'),
    path('sessions/<int:pk>/', views.session_detail, name='session_detail'),
    path('session/ajouter/', views.session_create, name='session_create'),
    path('sessions/<int:session_id>/commentaires/', views.commentaire_list, name='commentaire_list'),

    # Routes pour les Commentaires
    path('commentaires/', views.commentaire_list, name='commentaire_list'),
    path(
        'sessions/<int:session_id>/commentaire/ajouter/',
        views.commentaire_create,
        name='commentaire_create'
    ),

    # Routes pour l'Authentification
    path('register/', views.register, name='register'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]

