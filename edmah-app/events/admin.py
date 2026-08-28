from django.contrib import admin

from .models import Event, EventRegistration


class EventRegistrationInline(admin.TabularInline):
    model = EventRegistration
    extra = 0
    readonly_fields = ('created_at',)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'event_type', 'start_datetime', 'capacity', 'seats_taken', 'is_published')
    list_filter = ('event_type', 'is_published')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [EventRegistrationInline]


@admin.register(EventRegistration)
class EventRegistrationAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'event', 'status', 'created_at')
    list_filter = ('status', 'event')
    search_fields = ('full_name', 'email')
