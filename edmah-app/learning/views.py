import json

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from admissions.models import Inscription
from catalog.models import Formation
from certificates.services import issue_certificate_if_eligible

from .models import Attempt, Course, Module, Note, Progress


def _enrolled_formations(user):
    formation_ids = Inscription.objects.filter(
        user=user, status=Inscription.Status.ACCEPTE
    ).values_list('formation_id', flat=True)
    return Formation.objects.filter(id__in=formation_ids, course__isnull=False)


@login_required
def dashboard(request):
    formations = _enrolled_formations(request.user)
    return render(request, 'learning/dashboard.html', {'formations': formations})


@login_required
def course_detail(request, slug):
    formation = get_object_or_404(Formation, slug=slug)
    course = get_object_or_404(Course, formation=formation)

    if not _enrolled_formations(request.user).filter(id=formation.id).exists() and not request.user.is_staff:
        return redirect('inscriptions')

    modules = list(course.modules.prefetch_related('quiz__questions__choices', 'resources'))
    completed_ids = set(
        Progress.objects.filter(user=request.user, module__in=modules, completed=True)
        .values_list('module_id', flat=True)
    )

    unlocked_ids = set()
    for i, module in enumerate(modules):
        if i == 0 or modules[i - 1].id in completed_ids:
            unlocked_ids.add(module.id)

    module_id = request.GET.get('module')
    current_module = None
    if module_id:
        current_module = next((m for m in modules if str(m.id) == str(module_id)), None)
    if current_module is None:
        current_module = next((m for m in modules if m.id not in completed_ids), modules[0] if modules else None)

    if current_module and current_module.id not in unlocked_ids:
        current_module = next((m for m in modules if m.id in unlocked_ids), None)

    note = None
    if current_module:
        note = Note.objects.filter(user=request.user, module=current_module).first()

    progress_percent = int(len(completed_ids) / len(modules) * 100) if modules else 0

    context = {
        'formation': formation,
        'course': course,
        'modules': modules,
        'completed_ids': completed_ids,
        'unlocked_ids': unlocked_ids,
        'current_module': current_module,
        'note': note,
        'progress_percent': progress_percent,
        'completed_count': len(completed_ids),
    }
    return render(request, 'learning/course_detail.html', context)


@login_required
@require_POST
def submit_quiz(request, module_id):
    module = get_object_or_404(Module, pk=module_id)
    quiz = getattr(module, 'quiz', None)
    if quiz is None:
        return JsonResponse({'message': 'Aucun quiz pour ce module.'}, status=400)

    try:
        answers = json.loads(request.body.decode('utf-8'))
    except (ValueError, UnicodeDecodeError):
        answers = {}

    questions = list(quiz.questions.prefetch_related('choices'))
    correct = 0
    for question in questions:
        selected_id = answers.get(str(question.id))
        if selected_id and question.choices.filter(id=selected_id, is_correct=True).exists():
            correct += 1

    score = int(correct / len(questions) * 100) if questions else 0
    passed = score >= quiz.pass_threshold

    Attempt.objects.create(quiz=quiz, user=request.user, score=score, passed=passed)

    certificate_issued = False
    if passed:
        Progress.objects.update_or_create(
            user=request.user, module=module,
            defaults={'completed': True, 'completed_at': timezone.now()},
        )
        certificate = issue_certificate_if_eligible(request.user, module.course)
        certificate_issued = certificate is not None

    return JsonResponse({
        'score': score,
        'passed': passed,
        'threshold': quiz.pass_threshold,
        'certificate_issued': certificate_issued,
    })


@login_required
@require_POST
def save_note(request, module_id):
    module = get_object_or_404(Module, pk=module_id)
    try:
        payload = json.loads(request.body.decode('utf-8'))
    except (ValueError, UnicodeDecodeError):
        payload = {}

    note, _created = Note.objects.update_or_create(
        user=request.user, module=module,
        defaults={'content': payload.get('content', '')},
    )
    return JsonResponse({'saved': True, 'updated_at': note.updated_at.isoformat()})
