from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import (
    MotsCles,
    CentreFormation,
    Personne,
    Formation,
    SessionFormation,
    Commentaire
)
from datetime import date, datetime

class MotsClesModelTest(TestCase):
    def setUp(self):
        self.mot_cle = MotsCles.objects.create(mot='Python')

    def test_mot_cle_str(self):
        self.assertEqual(str(self.mot_cle), 'Python')


class CentreFormationModelTest(TestCase):
    def setUp(self):
        self.mot_cle = MotsCles.objects.create(mot='Python')
        self.centre = CentreFormation.objects.create(
            nom='Centre de Formation Django',
            adresse='123 Rue de l\'Exemple',
            ville='Paris',
            code_postal='75001',
            pays='France',
            telephone='0123456789',
            email='contact@example.com',
            site_web='http://www.example.com',
            description='Description du centre de formation',
            latitude=48.856613,
            longitude=2.352222
        )
        self.centre.mots_cles.add(self.mot_cle)

    def test_centre_formation_str(self):
        self.assertEqual(str(self.centre), 'Centre de Formation Django')

    def test_mots_cles_relationship(self):
        self.assertIn(self.mot_cle, self.centre.mots_cles.all())


class PersonneModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.mot_cle = MotsCles.objects.create(mot='Python')
        self.personne = Personne.objects.create(
            user=self.user,
            telephone='0987654321',
            date_naissance=date(1990, 1, 1),
            adresse='456 Rue de l\'Exemple'
        )
        self.personne.attentes.add(self.mot_cle)

    def test_personne_str(self):
        self.assertEqual(str(self.personne), 'testuser')

    def test_attentes_relationship(self):
        self.assertIn(self.mot_cle, self.personne.attentes.all())


class FormationModelTest(TestCase):
    def setUp(self):
        self.centre = CentreFormation.objects.create(
            nom='Centre de Formation Django',
            adresse='123 Rue de l\'Exemple',
            ville='Paris',
            code_postal='75001',
            pays='France'
        )
        self.formation = Formation.objects.create(
            titre='Formation Django',
            description='Description de la formation',
            centre_formation=self.centre,
            date_debut=date(2024, 1, 1),
            date_fin=date(2024, 1, 15),
            niveau='Débutant'
        )

    def test_formation_str(self):
        self.assertEqual(str(self.formation), 'Formation Django')

    def test_duree(self):
        self.assertEqual(self.formation.duree(), 14)


class SessionFormationModelTest(TestCase):
    def setUp(self):
        self.centre = CentreFormation.objects.create(
            nom='Centre de Formation Django',
            adresse='123 Rue de l\'Exemple',
            ville='Paris',
            code_postal='75001',
            pays='France'
        )
        self.formation = Formation.objects.create(
            titre='Formation Django',
            description='Description de la formation',
            centre_formation=self.centre,
            date_debut=date(2024, 1, 1),
            date_fin=date(2024, 1, 15),
            niveau='Débutant'
        )
        self.user = User.objects.create_user(username='formateur', password='password')
        self.personne = Personne.objects.create(user=self.user, date_naissance=date(1980, 1, 1))
        self.session = SessionFormation.objects.create(
            formation=self.formation,
            date_debut=date(2024, 1, 5),
            date_fin=date(2024, 1, 10),
            lieu='Salle 101',
            formateur=self.personne
        )

    def test_session_formation_str(self):
        self.assertEqual(str(self.session), 'Formation Django - 05/01/2024')


class CommentaireModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.centre = CentreFormation.objects.create(
            nom='Centre de Formation Django',
            adresse='123 Rue de l\'Exemple',
            ville='Paris',
            code_postal='75001',
            pays='France'
        )
        self.formation = Formation.objects.create(
            titre='Formation Django',
            description='Description de la formation',
            centre_formation=self.centre,
            date_debut=date(2024, 1, 1),
            date_fin=date(2024, 1, 15),
            niveau='Débutant'
        )
        self.session = SessionFormation.objects.create(
            formation=self.formation,
            date_debut=date(2024, 1, 5),
            date_fin=date(2024, 1, 10),
            lieu='Salle 101'
        )
        self.commentaire = Commentaire.objects.create(
            auteur=self.user,
            texte='Super formation !',
            session_formation=self.session
        )


class MotsClesTests(TestCase):
    def test_mots_cles_creation(self):
        mot_cle = MotsCles.objects.create(mot='Python')
        self.assertEqual(mot_cle.mot, 'Python')
        self.assertEqual(str(mot_cle), 'Python')

    def test_mots_cles_uniqueness(self):
        MotsCles.objects.create(mot='UniqueMot')
        with self.assertRaises(Exception):
            MotsCles.objects.create(mot='UniqueMot')


class CentreFormationTests(TestCase):
    def setUp(self):
        self.mot_cle = MotsCles.objects.create(mot='Informatique')

    def test_centre_formation_creation(self):
        centre = CentreFormation.objects.create(
            nom='Centre de Test',
            adresse='123 Rue de Test',
            ville='TestVille',
            code_postal='12345',
            pays='France',
            telephone='0123456789',
            email='test@centre.com',
            site_web='http://www.centre.com',
            description='Description du centre de test'
        )
        centre.mots_cles.add(self.mot_cle)

        self.assertEqual(centre.nom, 'Centre de Test')
        self.assertIn(self.mot_cle, centre.mots_cles.all())
        self.assertEqual(str(centre), 'Centre de Test')

    def test_centre_formation_default_values(self):
        centre = CentreFormation.objects.create(
            nom='Centre Default',
            ville='VilleDefault',
            pays='PaysDefault'
        )
        self.assertEqual(centre.adresse, 'Adresse par défaut')
        self.assertEqual(centre.code_postal, '00000')


class PersonneTests(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser', password='testpass')
        self.mot_cle = MotsCles.objects.create(mot='Marketing')

    def test_personne_creation(self):
        personne = Personne.objects.create(
            user=self.user,
            telephone='0123456789',
            date_naissance=date(1990, 1, 1),
            adresse='123 Rue de Test'
        )
        personne.attentes.add(self.mot_cle)

        self.assertEqual(personne.user.username, 'testuser')
        self.assertIn(self.mot_cle, personne.attentes.all())
        self.assertEqual(str(personne), 'testuser')


class FormationTests(TestCase):
    def setUp(self):
        self.centre = CentreFormation.objects.create(
            nom='Centre Test',
            ville='VilleTest',
            pays='France'
        )

    def test_formation_creation(self):
        formation = Formation.objects.create(
            titre='Formation Test',
            description='Description de la formation test',
            centre_formation=self.centre,
            date_debut=date(2024, 9, 1),
            date_fin=date(2024, 9, 5),
            niveau='Débutant'
        )

        self.assertEqual(formation.titre, 'Formation Test')
        self.assertEqual(formation.duree(), 4)
        self.assertEqual(str(formation), 'Formation Test')


class SessionFormationTests(TestCase):
    def setUp(self):
        self.centre = CentreFormation.objects.create(
            nom='Centre Test',
            ville='VilleTest',
            pays='France'
        )
        self.formation = Formation.objects.create(
            titre='Formation Test',
            description='Description de la formation test',
            centre_formation=self.centre,
            date_debut=date(2024, 9, 1),
            date_fin=date(2024, 9, 5),
            niveau='Débutant'
        )
        self.user = User.objects.create(username='testformateur', password='testpass')
        self.formateur = Personne.objects.create(
            user=self.user,
            date_naissance=date(1985, 5, 5)
        )

    def test_session_formation_creation(self):
        session = SessionFormation.objects.create(
            formation=self.formation,
            date_debut=datetime(2024, 9, 1, 10, 0),
            date_fin=datetime(2024, 9, 5, 15, 0),
            lieu='Salle 101',
            formateur=self.formateur
        )

        self.assertEqual(session.formation.titre, 'Formation Test')
        self.assertEqual(str(session), 'Formation Test - 01/09/2024')


class CommentaireTests(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='commentateur', password='testpass')
        self.centre = CentreFormation.objects.create(
            nom='Centre Commentaire',
            ville='VilleCommentaire',
            pays='France'
        )
        self.formation = Formation.objects.create(
            titre='Formation Commentaire',
            description='Description de la formation',
            centre_formation=self.centre,
            date_debut=date(2024, 10, 1),
            date_fin=date(2024, 10, 10),
            niveau='Avancé'
        )
        self.session = SessionFormation.objects.create(
            formation=self.formation,
            date_debut=datetime(2024, 10, 1, 9, 0),
            date_fin=datetime(2024, 10, 10, 17, 0),
            lieu='Salle A'
        )

    def test_commentaire_creation(self):
        commentaire = Commentaire.objects.create(
            auteur=self.user,
            texte='Très bon cours!',
            session_formation=self.session
        )

        self.assertEqual(commentaire.auteur.username, 'commentateur')
        self.assertEqual(commentaire.texte, 'Très bon cours!')


class HomePageTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.centre = CentreFormation.objects.create(
            nom='Centre de Test',
            ville='VilleTest',
            pays='France'
        )
        self.formation = Formation.objects.create(
            titre='Formation Test',
            description='Description de la formation test',
            centre_formation=self.centre,
            date_debut=date(2024, 9, 1),
            date_fin=date(2024, 9, 5),
            niveau='Débutant'
        )
        self.formateur = Personne.objects.create(
            user=self.user,
            date_naissance=date(1985, 5, 5)
        )
        self.session = SessionFormation.objects.create(
            formation=self.formation,
            date_debut=datetime(2024, 9, 1, 10, 0),
            date_fin=datetime(2024, 9, 5, 15, 0),
            lieu='Salle 101',
            formateur=self.formateur
        )
        self.commentaire = Commentaire.objects.create(
            auteur=self.user,
            texte='Super session!',
            session_formation=self.session
        )
