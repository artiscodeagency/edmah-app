from django.db import models


class Event(models.Model):
    class EventType(models.TextChoices):
        PRESENTIEL = 'presentiel', 'Présentiel'
        WEBINAIRE = 'webinaire', 'Webinaire en ligne'

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True)
    event_type = models.CharField(max_length=20, choices=EventType.choices, default=EventType.PRESENTIEL)
    description = models.TextField()
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField(blank=True, null=True)
    location = models.CharField(max_length=200, blank=True, help_text='Adresse ou "En ligne (Zoom)"')
    capacity = models.PositiveIntegerField(default=50)
    price = models.DecimalField(max_digits=10, decimal_places=0, default=0, help_text='0 = gratuit')
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ['start_datetime']

    def __str__(self):
        return self.title

    @property
    def is_past(self):
        from django.utils import timezone
        return self.start_datetime < timezone.now()

    @property
    def seats_taken(self):
        return self.registrations.filter(status__in=['confirme', 'en_attente']).count()

    @property
    def seats_available(self):
        return max(self.capacity - self.seats_taken, 0)


class EventRegistration(models.Model):
    class Status(models.TextChoices):
        EN_ATTENTE = 'en_attente', 'En attente'
        CONFIRME = 'confirme', 'Confirmé'
        ANNULE = 'annule', 'Annulé'

    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='registrations')
    full_name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=30, blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.EN_ATTENTE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        constraints = [
            models.UniqueConstraint(fields=['event', 'email'], name='unique_event_registration_email')
        ]

    def __str__(self):
        return f'{self.full_name} — {self.event}'
