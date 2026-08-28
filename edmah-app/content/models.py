from django.conf import settings
from django.db import models
from django.urls import reverse


class ArticleCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    badge_class = models.CharField(max_length=40, default='bg-info text-dark', help_text='Classes Bootstrap du badge')

    class Meta:
        verbose_name_plural = 'Article categories'
        ordering = ['name']

    def __str__(self):
        return self.name


class Article(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True)
    category = models.ForeignKey(ArticleCategory, on_delete=models.PROTECT, related_name='articles')
    author_name = models.CharField(max_length=120)
    excerpt = models.TextField()
    body = models.TextField(blank=True)
    cover_image = models.ImageField(upload_to='articles/', blank=True, null=True)
    is_published = models.BooleanField(default=True)
    published_at = models.DateTimeField()

    class Meta:
        ordering = ['-published_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('article_detail', args=[self.slug])


class GalleryItem(models.Model):
    class MediaType(models.TextChoices):
        PHOTO = 'photo', 'Photo'
        VIDEO = 'video', 'Vidéo'

    title = models.CharField(max_length=150)
    subtitle = models.CharField(max_length=200, blank=True)
    media_type = models.CharField(max_length=10, choices=MediaType.choices, default=MediaType.PHOTO)
    image = models.ImageField(upload_to='gallery/', blank=True, null=True)
    video_url = models.URLField(blank=True)
    category = models.CharField(max_length=60, blank=True, help_text='Ex: evenements, temoignages')
    is_published = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', '-id']

    def __str__(self):
        return self.title


class FAQ(models.Model):
    question = models.CharField(max_length=250)
    answer = models.TextField()
    order = models.PositiveIntegerField(default=0)
    is_published = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'FAQ'
        verbose_name_plural = 'FAQ'
        ordering = ['order']

    def __str__(self):
        return self.question
