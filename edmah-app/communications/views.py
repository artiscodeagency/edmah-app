import json

from django.conf import settings
from django.core.mail import send_mail
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from .models import ContactMessage, NewsletterSubscriber


def _parse_json(request):
    try:
        return json.loads(request.body.decode('utf-8'))
    except (ValueError, UnicodeDecodeError):
        return {}


@require_POST
def contact_submit(request):
    payload = _parse_json(request) or request.POST
    name = (payload.get('name') or '').strip()
    email = (payload.get('email') or '').strip()
    subject = (payload.get('subject') or '').strip()
    message = (payload.get('message') or '').strip()

    if not all([name, email, subject, message]):
        return JsonResponse({'message': 'Tous les champs obligatoires doivent être remplis.'}, status=400)

    contact = ContactMessage.objects.create(name=name, email=email, subject=subject, message=message)

    send_mail(
        subject=f"EDMAH — Nouveau message de contact : {subject}",
        message=f"De: {name} <{email}>\n\n{message}",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[settings.ADMIN_NOTIFICATION_EMAIL],
        fail_silently=True,
    )

    return JsonResponse({'message': 'Votre message a bien été envoyé. Notre équipe vous répondra rapidement.', 'id': contact.id}, status=201)


@require_POST
def newsletter_subscribe(request):
    payload = _parse_json(request) or request.POST
    email = (payload.get('email') or '').strip()
    if not email:
        return JsonResponse({'message': 'Adresse email invalide.'}, status=400)

    subscriber, created = NewsletterSubscriber.objects.get_or_create(email=email)
    if not created and not subscriber.is_active:
        subscriber.is_active = True
        subscriber.save(update_fields=['is_active'])

    return JsonResponse({'message': 'Merci ! Vous êtes maintenant inscrit à notre newsletter.'}, status=201)
