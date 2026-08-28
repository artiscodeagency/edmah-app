from django.db import migrations


MODEL_PERMS = {
    'course': ['view_course', 'change_course'],
    'module': ['add_module', 'change_module', 'delete_module', 'view_module'],
    'resource': ['add_resource', 'change_resource', 'delete_resource', 'view_resource'],
    'quiz': ['add_quiz', 'change_quiz', 'delete_quiz', 'view_quiz'],
    'question': ['add_question', 'change_question', 'delete_question', 'view_question'],
    'choice': ['add_choice', 'change_choice', 'delete_choice', 'view_choice'],
    'attempt': ['view_attempt'],
    'progress': ['view_progress'],
}


def grant_formateur_permissions(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    Permission = apps.get_model('auth', 'Permission')

    group, _created = Group.objects.get_or_create(name='Formateurs')

    codenames = [codename for perms in MODEL_PERMS.values() for codename in perms]
    permissions = Permission.objects.filter(
        content_type__app_label='learning', codename__in=codenames
    )
    group.permissions.add(*permissions)


def revoke_formateur_permissions(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    Group.objects.filter(name='Formateurs').delete()


class Migration(migrations.Migration):

    dependencies = [
        ('learning', '0002_course_instructors'),
    ]

    operations = [
        migrations.RunPython(grant_formateur_permissions, revoke_formateur_permissions),
    ]
