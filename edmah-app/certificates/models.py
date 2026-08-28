import uuid

from django.conf import settings
from django.db import models

from catalog.models import Formation


def generate_certificate_code():
    from django.utils import timezone
    return f'EDMAH-{timezone.now().year}-CERT-{uuid.uuid4().hex[:6].upper()}'


class Certificate(models.Model):
    code = models.CharField(max_length=40, unique=True, default=generate_certificate_code, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='certificates')
    formation = models.ForeignKey(Formation, on_delete=models.CASCADE, related_name='certificates')
    issued_at = models.DateTimeField(auto_now_add=True)
    is_revoked = models.BooleanField(default=False)

    class Meta:
        unique_together = [('user', 'formation')]
        ordering = ['-issued_at']

    def __str__(self):
        return f'{self.code} — {self.user} — {self.formation}'
