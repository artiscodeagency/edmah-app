from django.http import JsonResponse

from .models import Certificate


def verify_certificate(request):
    code = (request.GET.get('code') or '').strip()
    if not code:
        return JsonResponse({'valid': False, 'message': 'Veuillez fournir un code de certificat.'}, status=400)

    certificate = Certificate.objects.filter(code__iexact=code, is_revoked=False).select_related('user', 'formation').first()
    if not certificate:
        return JsonResponse({'valid': False, 'message': 'Aucun certificat valide ne correspond à ce code.'}, status=404)

    return JsonResponse({
        'valid': True,
        'holder': certificate.user.get_full_name() or certificate.user.username,
        'formation': certificate.formation.title,
        'issued_at': certificate.issued_at.strftime('%d %B %Y'),
        'code': certificate.code,
    })
