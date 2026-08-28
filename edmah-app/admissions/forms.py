from django import forms
from django.conf import settings

from .models import Inscription


class InscriptionForm(forms.ModelForm):
    class Meta:
        model = Inscription
        fields = [
            'last_name', 'first_name', 'birth_date', 'gender', 'email', 'phone',
            'marital_status', 'address', 'formation', 'session', 'mode',
            'motivations', 'id_photo', 'civil_document',
        ]

    def clean_id_photo(self):
        photo = self.cleaned_data['id_photo']
        if photo.size > settings.MAX_ID_PHOTO_SIZE:
            raise forms.ValidationError("La photo d'identité dépasse la taille maximale de 2 Mo.")
        if photo.content_type not in ('image/jpeg', 'image/png'):
            raise forms.ValidationError("La photo d'identité doit être au format JPEG ou PNG.")
        return photo

    def clean_civil_document(self):
        doc = self.cleaned_data['civil_document']
        if doc.size > settings.MAX_DOCUMENT_SIZE:
            raise forms.ValidationError("Le document d'état civil dépasse la taille maximale de 5 Mo.")
        allowed = ('image/jpeg', 'image/png', 'application/pdf')
        if doc.content_type not in allowed:
            raise forms.ValidationError("Le document d'état civil doit être une image ou un PDF.")
        return doc
