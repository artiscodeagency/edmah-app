from django.contrib import admin

from .models import Category, Formation, FormationHighlight, Session


class FormationHighlightInline(admin.TabularInline):
    model = FormationHighlight
    extra = 1


class SessionInline(admin.TabularInline):
    model = Session
    extra = 0


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Formation)
class FormationAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'mode', 'price', 'is_published', 'is_featured', 'order')
    list_filter = ('category', 'mode', 'is_published')
    search_fields = ('title', 'short_description')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [FormationHighlightInline, SessionInline]


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ('formation', 'start_date', 'capacity', 'seats_taken', 'is_open')
    list_filter = ('is_open', 'formation')
