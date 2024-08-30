from django.db import models
from django.contrib.auth.models import User


class MotsCles(models.Model):
    """Modèle représentant les mots-clés pour les formations."""
    
    mot = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.mot


class CentreFormation(models.Model):
    """Modèle représentant un centre de formation."""
    
    nom = models.CharField(max_length=100)
    adresse = models.CharField(max_length=255, default='Adresse par défaut')
    ville = models.CharField(max_length=100)
    code_postal = models.CharField(max_length=20, default='00000')
    pays = models.CharField(max_length=100)
    telephone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    site_web = models.URLField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    mots_cles = models.ManyToManyField(MotsCles, related_name='centres_formation', blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    def __str__(self):
        return self.nom


class Personne(models.Model):
    """Modèle représentant une personne liée à un utilisateur Django."""
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    telephone = models.CharField(max_length=20, blank=True, null=True)
    date_naissance = models.DateField()
    adresse = models.CharField(max_length=255, blank=True, null=True)
    attentes = models.ManyToManyField(MotsCles, related_name='personnes', blank=True)

    def __str__(self):
        return self.user.username


class Formation(models.Model):
    """Modèle représentant une formation dans un centre de formation."""
    
    titre = models.CharField(max_length=255)
    description = models.TextField()
    centre_formation = models.ForeignKey(
        CentreFormation, on_delete=models.CASCADE, related_name='formations'
    )
    date_debut = models.DateField()
    date_fin = models.DateField()
    niveau = models.CharField(max_length=100)

    def __str__(self):
        return self.titre

    def duree(self):
        """Retourne la durée de la formation en jours."""
        return (self.date_fin - self.date_debut).days


class SessionFormation(models.Model):
    """Modèle représentant une session de formation."""
    
    formation = models.ForeignKey(
        Formation, on_delete=models.CASCADE, related_name='sessions'
    )
    date_debut = models.DateTimeField()
    date_fin = models.DateTimeField()
    lieu = models.CharField(max_length=255)
    formateur = models.ForeignKey(
        Personne, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='sessions'
    )

    def __str__(self):
        return f"{self.formation.titre} - {self.date_debut.strftime('%d/%m/%Y')}"


class Commentaire(models.Model):
    """Modèle représentant un commentaire sur une session de formation."""
    
    auteur = models.ForeignKey(User, on_delete=models.CASCADE)
    date_commentaire = models.DateTimeField(auto_now_add=True)
    texte = models.TextField()
    session_formation = models.ForeignKey(
        SessionFormation, on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.auteur.username} - {self.date_commentaire}"
