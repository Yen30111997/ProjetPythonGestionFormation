from django.contrib import admin
from .models import CentreFormation, Personne, Formation, SessionFormation, Commentaire


@admin.register(CentreFormation)
class CentreFormationAdmin(admin.ModelAdmin):
    list_display = ['nom', 'adresse', 'site_web']
    search_fields = ['nom', 'adresse']


@admin.register(Personne)
class PersonneAdmin(admin.ModelAdmin):
    list_display = ['user', 'telephone', 'date_naissance', 'adresse']
    search_fields = ['user__username', 'telephone', 'adresse']
    list_filter = ['date_naissance']


@admin.register(Formation)
class FormationAdmin(admin.ModelAdmin):
    list_display = ['titre', 'description', 'centre_formation', 'date_debut', 'date_fin', 'niveau']
    search_fields = ['titre', 'description']
    list_filter = ['date_debut', 'date_fin', 'niveau']
    raw_id_fields = ['centre_formation']


@admin.register(SessionFormation)
class SessionFormationAdmin(admin.ModelAdmin):
    list_display = ['formation', 'date_debut', 'date_fin', 'lieu', 'formateur']
    search_fields = ['formation__titre', 'lieu', 'formateur']
    list_filter = ['date_debut', 'date_fin']
    raw_id_fields = ['formation']


@admin.register(Commentaire)
class CommentaireAdmin(admin.ModelAdmin):
    list_display = ['session_formation', 'auteur', 'texte', 'date_commentaire']
    search_fields = ['texte', 'auteur__user__username']
    list_filter = ['date_commentaire']
    raw_id_fields = ['session_formation', 'auteur']