from django.contrib.auth.models import AbstractUser
from django.db import models

class Utilisateur(AbstractUser):
    ROLE_CHOICES = [
        ('user', 'User'),
        ('admin', 'Admin'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')

class ProduitChimique(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField()
    concentration = models.FloatField()

class CalculateurDeDosage(models.Model):
    # Ajoutez ici les champs nécessaires pour gérer les calculs de dosage
    pass
