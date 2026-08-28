from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.http import FileResponse, Http404, JsonResponse
from django.utils.datastructures import MultiValueDict
from django.views.decorators.http import require_POST

from catalog.models import Formation

from .forms import InscriptionForm
from .models import AdmissionDocument
from .storage import private_storage

FIELD_MAP = {
    'lastName': 'last_name',
    'firstName': 'first_name',
    'birthDate': 'birth_date',
    'gender': 'gender',
    'email': 'email',
    'phone': 'phone',
    'maritalStatus': 'marital_status',
    'address': 'address',
    'formation': 'formation',
    'session': 'session',
    'mode': 'mode',
    'motivations': 'motivations',
}

FILE_FIELD_MAP = {
    'idPhoto': 'id_photo',
    'civilDocument': 'civil_document',
}


@require_POST
def submit_inscription(request):
    data = {FIELD_MAP.get(key, key): value for key, value in request.POST.items()}

    formation_ref = data.get('formation')
    formation = Formation.objects.filter(slug=formation_ref).first() if formation_ref else None
    if formation is None:
        return JsonResponse({'message': "Formation sélectionnée introuvable."}, status=400)
    data['formation'] = formation.pk

    files = MultiValueDict({
        FILE_FIELD_MAP.get(key, key): request.FILES.getlist(key)
        for key in request.FILES
    })

    form = InscriptionForm(data, files)
    if not form.is_valid():
        errors = {field: [str(e) for e in errs] for field, errs in form.errors.items()}
        return JsonResponse({'message': "Veuillez corriger les erreurs du formulaire.", 'errors': errors}, status=400)

    inscription = form.save(commit=False)
    if request.user.is_authenticated:
        inscription.user = request.user
    inscription.save()

    for f in request.FILES.getlist('otherDocuments'):
        if f.size <= settings.MAX_DOCUMENT_SIZE:
            AdmissionDocument.objects.create(inscription=inscription, file=f)

    send_mail(
        subject="EDMAH — Confirmation de votre demande d'inscription",
        message=(
            f"Bonjour {inscription.first_name},\n\n"
            f"Votre demande d'inscription à la formation « {inscription.formation.title} » a bien été reçue "
            f"(référence {inscription.reference}).\nNotre équipe va l'étudier et reviendra vers vous rapidement.\n\n"
            "L'équipe EDMAH"
        ),
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[inscription.email],
        fail_silently=True,
    )
    send_mail(
        subject=f"Nouvelle inscription — {inscription.formation.title}",
        message=f"{inscription.full_name} ({inscription.email}) vient de s'inscrire à {inscription.formation.title}.",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[settings.ADMIN_NOTIFICATION_EMAIL],
        fail_silently=True,
    )

    return JsonResponse({
        'message': "Votre inscription a été enregistrée avec succès.",
        'reference': str(inscription.reference),
    }, status=201)


@login_required
def serve_document(request):
    """Streams a private admission document. Restricted to staff (back-office
    reviewers) since Django's admin is the only place these links are shown."""
    if not request.user.is_staff:
        raise Http404

    path = request.GET.get('path')
    if not path or not private_storage.exists(path):
        raise Http404

    return FileResponse(private_storage.open(path, 'rb'))
