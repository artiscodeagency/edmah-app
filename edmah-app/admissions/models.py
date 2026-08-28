import uuid

from django.conf import settings
from django.core.validators import FileExtensionValidator
from django.db import models

from catalog.models import Formation, Session

from .storage import private_storage


def admission_upload_path(instance, filename):
    return f'admissions/{instance.reference}/{filename}'


def admission_document_upload_path(instance, filename):
    return f'admissions/{instance.inscription.reference}/documents/{filename}'


class Inscription(models.Model):
    class MaritalStatus(models.TextChoices):
        CELIBATAIRE = 'celibataire', 'Célibataire'
        FIANCE = 'fiance', 'Fiancé(e)'
        MARIE = 'marie', 'Marié(e)'
        DIVORCE = 'divorce', 'Divorcé(e)'
        VEUF = 'veuf', 'Veuf/Veuve'

    class Mode(models.TextChoices):
        PRESENTIEL = 'presentiel', 'Présentiel'
        EN_LIGNE = 'en-ligne', 'En ligne'
        HYBRIDE = 'hybride', 'Hybride'

    class Gender(models.TextChoices):
        M = 'M', 'Masculin'
        F = 'F', 'Féminin'

    class Status(models.TextChoices):
        RECU = 'recu', 'Reçu'
        EN_COURS = 'en_cours', 'En cours de traitement'
        COMPLEMENT = 'complement', 'Complément demandé'
        ACCEPTE = 'accepte', 'Accepté'
        REFUSE = 'refuse', 'Refusé'

    reference = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True, related_name='inscriptions')

    # Étape 1 — Informations personnelles
    last_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    birth_date = models.DateField()
    gender = models.CharField(max_length=1, choices=Gender.choices)
    email = models.EmailField()
    phone = models.CharField(max_length=30)
    marital_status = models.CharField(max_length=20, choices=MaritalStatus.choices)
    address = models.TextField()

    # Étape 2 — Formation
    formation = models.ForeignKey(Formation, on_delete=models.PROTECT, related_name='inscriptions')
    session = models.ForeignKey(Session, on_delete=models.SET_NULL, blank=True, null=True, related_name='inscriptions')
    mode = models.CharField(max_length=20, choices=Mode.choices)
    motivations = models.TextField(blank=True)

    # Étape 3 — Documents
    id_photo = models.ImageField(upload_to=admission_upload_path, storage=private_storage)
    civil_document = models.FileField(
        upload_to=admission_upload_path,
        storage=private_storage,
        validators=[FileExtensionValidator(['pdf', 'jpg', 'jpeg', 'png'])],
    )

    # Suivi administratif
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.RECU)
    admin_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.first_name} {self.last_name} — {self.formation}'

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'


class AdmissionDocument(models.Model):
    inscription = models.ForeignKey(Inscription, on_delete=models.CASCADE, related_name='other_documents')
    file = models.FileField(
        upload_to=admission_document_upload_path,
        storage=private_storage,
        validators=[FileExtensionValidator(['pdf', 'jpg', 'jpeg', 'png'])],
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Document — {self.inscription}'
