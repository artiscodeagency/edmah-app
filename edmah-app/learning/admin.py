from django.contrib import admin

from .models import Attempt, Choice, Course, Module, Note, Progress, Question, Quiz, Resource


def _is_full_access(request):
    return request.user.is_superuser or getattr(request.user, 'role', None) == 'administrateur'


class InstructorScopedAdmin(admin.ModelAdmin):
    """Restricts formateurs to the courses they are assigned to as instructor.

    `course_lookup` is the ORM path from this model to Course, e.g.
    'course', 'module__course', 'quiz__module__course'.
    """
    course_lookup = 'course'

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if _is_full_access(request):
            return qs
        return qs.filter(**{f'{self.course_lookup}__instructors': request.user})

    def has_module_permission(self, request):
        return True


class ModuleInline(admin.StackedInline):
    model = Module
    extra = 0


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('formation', 'is_published')
    filter_horizontal = ('instructors',)
    inlines = [ModuleInline]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if _is_full_access(request):
            return qs
        return qs.filter(instructors=request.user)

    def has_add_permission(self, request):
        return _is_full_access(request)

    def has_delete_permission(self, request, obj=None):
        return _is_full_access(request)

    def get_readonly_fields(self, request, obj=None):
        if _is_full_access(request):
            return ()
        return ('formation', 'is_published', 'instructors')


class ResourceInline(admin.TabularInline):
    model = Resource
    extra = 0


@admin.register(Module)
class ModuleAdmin(InstructorScopedAdmin):
    course_lookup = 'course'
    list_display = ('course', 'order', 'title')
    list_filter = ('course',)
    inlines = [ResourceInline]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'course' and not _is_full_access(request):
            kwargs['queryset'] = Course.objects.filter(instructors=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class QuestionInline(admin.StackedInline):
    model = Question
    extra = 1


@admin.register(Quiz)
class QuizAdmin(InstructorScopedAdmin):
    course_lookup = 'module__course'
    list_display = ('module', 'pass_threshold')
    inlines = [QuestionInline]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'module' and not _is_full_access(request):
            kwargs['queryset'] = Module.objects.filter(course__instructors=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3


@admin.register(Question)
class QuestionAdmin(InstructorScopedAdmin):
    course_lookup = 'quiz__module__course'
    list_display = ('text', 'quiz', 'order')
    inlines = [ChoiceInline]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'quiz' and not _is_full_access(request):
            kwargs['queryset'] = Quiz.objects.filter(module__course__instructors=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Attempt)
class AttemptAdmin(InstructorScopedAdmin):
    course_lookup = 'quiz__module__course'
    list_display = ('user', 'quiz', 'score', 'passed', 'created_at')
    list_filter = ('passed', 'quiz')

    def has_add_permission(self, request):
        return _is_full_access(request)

    def has_change_permission(self, request, obj=None):
        return _is_full_access(request)


@admin.register(Progress)
class ProgressAdmin(InstructorScopedAdmin):
    course_lookup = 'module__course'
    list_display = ('user', 'module', 'completed', 'completed_at')
    list_filter = ('completed',)

    def has_add_permission(self, request):
        return _is_full_access(request)

    def has_change_permission(self, request, obj=None):
        return _is_full_access(request)


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('user', 'module', 'updated_at')

    def has_module_permission(self, request):
        return _is_full_access(request)
