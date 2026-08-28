from django.contrib import admin

from .models import Attempt, Choice, Course, Module, Note, Progress, Question, Quiz, Resource


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3


class QuestionInline(admin.StackedInline):
    model = Question
    extra = 1


class ResourceInline(admin.TabularInline):
    model = Resource
    extra = 0


class ModuleInline(admin.StackedInline):
    model = Module
    extra = 0


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('formation', 'is_published')
    inlines = [ModuleInline]


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ('course', 'order', 'title')
    list_filter = ('course',)
    inlines = [ResourceInline]


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('module', 'pass_threshold')
    inlines = [QuestionInline]


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'quiz', 'order')
    inlines = [ChoiceInline]


@admin.register(Attempt)
class AttemptAdmin(admin.ModelAdmin):
    list_display = ('user', 'quiz', 'score', 'passed', 'created_at')
    list_filter = ('passed', 'quiz')


@admin.register(Progress)
class ProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'module', 'completed', 'completed_at')
    list_filter = ('completed',)


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('user', 'module', 'updated_at')
