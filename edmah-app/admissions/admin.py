from django.contrib import admin

from .models import AdmissionDocument, Inscription


class AdmissionDocumentInline(admin.TabularInline):
    model = AdmissionDocument
    extra = 0
    readonly_fields = ('uploaded_at',)


@admin.register(Inscription)
class InscriptionAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'formation', 'mode', 'status', 'created_at')
    list_filter = ('status', 'formation', 'mode')
    search_fields = ('first_name', 'last_name', 'email', 'phone')
    readonly_fields = ('reference', 'created_at', 'updated_at')
    inlines = [AdmissionDocumentInline]
    actions = ['mark_accepted', 'mark_refused', 'mark_in_progress']

    @admin.action(description="Marquer comme accepté")
    def mark_accepted(self, request, queryset):
        queryset.update(status=Inscription.Status.ACCEPTE)

    @admin.action(description="Marquer comme refusé")
    def mark_refused(self, request, queryset):
        queryset.update(status=Inscription.Status.REFUSE)

    @admin.action(description="Marquer en cours de traitement")
    def mark_in_progress(self, request, queryset):
        queryset.update(status=Inscription.Status.EN_COURS)
