from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def __str__(self):
        return self.name


class Formation(models.Model):
    class Mode(models.TextChoices):
        PRESENTIEL = 'presentiel', 'Présentiel'
        EN_LIGNE = 'en-ligne', 'En ligne'
        HYBRIDE = 'hybride', 'Hybride'

    slug = models.SlugField(max_length=120, unique=True, help_text="Identifiant utilisé dans l'URL d'inscription")
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='formations')
    title = models.CharField(max_length=200)
    short_description = models.TextField()
    description = models.TextField(blank=True)
    duration_label = models.CharField(max_length=60, help_text='Ex: 8 semaines')
    sessions_label = models.CharField(max_length=60, blank=True, help_text='Ex: 16 sessions')
    audience = models.CharField(max_length=120, blank=True, help_text='Ex: Couples fiancés')
    mode = models.CharField(max_length=20, choices=Mode.choices, default=Mode.PRESENTIEL)
    price = models.DecimalField(max_digits=10, decimal_places=0, help_text='FCFA')
    image = models.ImageField(upload_to='formations/', blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    is_new = models.BooleanField(default=False)
    is_published = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', 'title']

    def __str__(self):
        return self.title

    def get_absolute_registration_url(self):
        return f"{reverse('inscriptions')}?formation={self.slug}"


class FormationHighlight(models.Model):
    formation = models.ForeignKey(Formation, on_delete=models.CASCADE, related_name='highlights')
    icon = models.CharField(max_length=40, default='fa-check', help_text='Classe FontAwesome, ex: fa-check')
    title = models.CharField(max_length=150)
    description = models.CharField(max_length=200, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f'{self.formation} — {self.title}'


class Session(models.Model):
    formation = models.ForeignKey(Formation, on_delete=models.CASCADE, related_name='sessions')
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    capacity = models.PositiveIntegerField(default=20)
    location = models.CharField(max_length=200, blank=True)
    is_open = models.BooleanField(default=True)

    class Meta:
        ordering = ['start_date']

    def __str__(self):
        return f'{self.formation} — {self.start_date}'

    @property
    def seats_taken(self):
        return self.inscriptions.filter(status__in=['recu', 'en_cours', 'accepte']).count()

    @property
    def seats_available(self):
        return max(self.capacity - self.seats_taken, 0)
