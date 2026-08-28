import json

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST

from .models import Event, EventRegistration


@require_POST
def register_for_event(request, slug):
    event = get_object_or_404(Event, slug=slug, is_published=True)

    try:
        payload = json.loads(request.body.decode('utf-8'))
    except (ValueError, UnicodeDecodeError):
        payload = request.POST

    full_name = (payload.get('full_name') or '').strip()
    email = (payload.get('email') or '').strip()
    phone = (payload.get('phone') or '').strip()

    if not full_name or not email:
        return JsonResponse({'message': 'Le nom et l\'email sont obligatoires.'}, status=400)

    if EventRegistration.objects.filter(event=event, email=email).exists():
        return JsonResponse({'message': 'Vous êtes déjà inscrit à cet événement.'}, status=200)

    if event.seats_available <= 0:
        return JsonResponse({'message': "Cet événement est complet."}, status=400)

    EventRegistration.objects.create(event=event, email=email, full_name=full_name, phone=phone)

    return JsonResponse({'message': 'Votre inscription à l\'événement a bien été enregistrée.'}, status=201)
