from django.conf import settings
from django.db import models

from catalog.models import Formation


class Course(models.Model):
    formation = models.OneToOneField(Formation, on_delete=models.CASCADE, related_name='course')
    is_published = models.BooleanField(default=True)

    def __str__(self):
        return f'Cours — {self.formation}'


class Module(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='modules')
    order = models.PositiveIntegerField(default=1)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    video_url = models.URLField(blank=True)
    duration_label = models.CharField(max_length=40, blank=True, help_text='Ex: 45 min')

    class Meta:
        ordering = ['order']
        unique_together = [('course', 'order')]

    def __str__(self):
        return f'{self.course.formation} — Module {self.order}: {self.title}'


class Resource(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='resources')
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to='learning/resources/')

    def __str__(self):
        return self.title


class Quiz(models.Model):
    module = models.OneToOneField(Module, on_delete=models.CASCADE, related_name='quiz')
    pass_threshold = models.PositiveIntegerField(default=80, help_text='Pourcentage requis pour valider')

    def __str__(self):
        return f'Quiz — {self.module}'


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()
    order = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.text[:60]


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    text = models.CharField(max_length=250)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text


class Attempt(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='attempts')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='quiz_attempts')
    score = models.PositiveIntegerField(help_text='Pourcentage obtenu')
    passed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user} — {self.quiz} — {self.score}%'


class Progress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='progress_entries')
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='progress_entries')
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        unique_together = [('user', 'module')]

    def __str__(self):
        return f'{self.user} — {self.module} — {"OK" if self.completed else "..."}'


class Note(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notes')
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='notes')
    content = models.TextField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = [('user', 'module')]

    def __str__(self):
        return f'Note {self.user} — {self.module}'
