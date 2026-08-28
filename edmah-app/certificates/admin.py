from django.contrib import admin

from .models import Certificate


@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ('code', 'user', 'formation', 'issued_at', 'is_revoked')
    list_filter = ('is_revoked', 'formation')
    search_fields = ('code', 'user__username', 'user__email')
    readonly_fields = ('code', 'issued_at')
