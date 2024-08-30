from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Commentaire, Formation, SessionFormation, Personne


# Formulaire pour les commentaires
class CommentaireForm(forms.ModelForm):
    class Meta:
        model = Commentaire
        fields = ['texte']
        widgets = {
            'texte': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Votre commentaire...'
            }),
        }


# Formulaire pour les formations
class FormationForm(forms.ModelForm):
    class Meta:
        model = Formation
        fields = [
            'titre',
            'description',
            'centre_formation',
            'date_debut',
            'date_fin',
            'niveau'
        ]
        widgets = {
            'description': forms.Textarea(attrs={
                'rows': 5,
                'placeholder': 'Description de la formation...'
            }),
            'date_debut': forms.DateInput(attrs={'type': 'date'}),
            'date_fin': forms.DateInput(attrs={'type': 'date'}),
        }


# Formulaire pour les sessions de formation
class SessionFormationForm(forms.ModelForm):
    class Meta:
        model = SessionFormation
        fields = ['formation', 'date_debut', 'date_fin', 'lieu', 'formateur']
        widgets = {
            'date_debut': forms.DateInput(attrs={'type': 'date'}),
            'date_fin': forms.DateInput(attrs={'type': 'date'}),
        }


# Formulaire pour les personnes
class PersonneForm(forms.ModelForm):
    class Meta:
        model = Personne
        fields = ['telephone', 'date_naissance', 'adresse', 'attentes']
        widgets = {
            'date_naissance': forms.DateInput(attrs={'type': 'date'}),
            'attentes': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Vos attentes...'
            }),
        }


# Formulaire personnalisé pour la création d'un utilisateur
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
