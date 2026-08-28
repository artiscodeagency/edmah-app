from .models import Certificate


def issue_certificate_if_eligible(user, course):
    """Delivers a certificate once every module of the course is completed by the user."""
    from learning.models import Progress

    module_ids = list(course.modules.values_list('id', flat=True))
    if not module_ids:
        return None

    completed_count = Progress.objects.filter(
        user=user, module_id__in=module_ids, completed=True
    ).count()

    if completed_count < len(module_ids):
        return None

    certificate, _created = Certificate.objects.get_or_create(
        user=user, formation=course.formation
    )
    return certificate
