from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Role(models.TextChoices):
        CANDIDAT = 'candidat', 'Candidat'
        APPRENANT = 'apprenant', 'Apprenant'
        FORMATEUR = 'formateur', 'Formateur'
        ADMIN = 'administrateur', 'Administrateur'

    role = models.CharField(max_length=20, choices=Role.choices, default=Role.CANDIDAT)
    phone = models.CharField(max_length=30, blank=True)

    def is_apprenant(self):
        return self.role == self.Role.APPRENANT

    def is_formateur(self):
        return self.role == self.Role.FORMATEUR

    def save(self, *args, **kwargs):
        # Un formateur a besoin d'accéder au back-office (vue restreinte à ses
        # cours) ; un administrateur a toujours accès complet.
        if self.role in (self.Role.FORMATEUR, self.Role.ADMIN):
            self.is_staff = True
        super().save(*args, **kwargs)
        if self.role == self.Role.FORMATEUR:
            from django.contrib.auth.models import Group
            group, _ = Group.objects.get_or_create(name='Formateurs')
            self.groups.add(group)

    def __str__(self):
        return self.get_full_name() or self.username
