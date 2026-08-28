from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone
from django.utils.text import slugify

from accounts.models import User
from admissions.models import Inscription
from catalog.models import Category, Formation, FormationHighlight, Session
from content.models import FAQ, Article, ArticleCategory, GalleryItem
from events.models import Event
from learning.models import Choice, Course, Module, Progress, Question, Quiz


class Command(BaseCommand):
    help = "Seed EDMAH demo data (catalog, content, events, learning) to bootstrap production."

    def handle(self, *args, **options):
        self.seed_catalog()
        self.seed_content()
        self.seed_events()
        self.seed_learning()
        self.stdout.write(self.style.SUCCESS('Demo data seeded successfully.'))

    def seed_catalog(self):
        categories = {
            'preparation': Category.objects.get_or_create(slug='preparation', defaults={'name': 'Préparation'})[0],
            'couple': Category.objects.get_or_create(slug='couple', defaults={'name': 'Vie de couple'})[0],
            'famille': Category.objects.get_or_create(slug='famille', defaults={'name': 'Famille'})[0],
        }

        formations_data = [
            dict(slug='preparation', category='preparation', title='Préparation au Mariage',
                 short_description="Un programme complet de 8 semaines pour préparer solidement votre union.",
                 duration_label='8 semaines', sessions_label='16 sessions', audience='Couples fiancés',
                 mode=Formation.Mode.PRESENTIEL, price=50000, is_featured=True),
            dict(slug='couple-epanoui', category='couple', title='Couple Épanoui',
                 short_description="Renforcez votre union et ravivez la flamme.",
                 duration_label='6 semaines', sessions_label='12 sessions', audience='Couples mariés',
                 mode=Formation.Mode.HYBRIDE, price=40000),
            dict(slug='gestion-familiale', category='famille', title='Gestion Familiale Biblique',
                 short_description="Apprenez à gérer votre foyer selon les principes de la Parole.",
                 duration_label='10 semaines', sessions_label='20 modules', audience='Parents',
                 mode=Formation.Mode.PRESENTIEL, price=60000),
            dict(slug='communication-conflits', category='couple', title='Communication & Résolution de Conflits',
                 short_description="Formation intensive pour améliorer votre communication.",
                 duration_label='4 semaines', sessions_label='8 sessions', audience='Tous couples',
                 mode=Formation.Mode.EN_LIGNE, price=30000, is_new=True),
            dict(slug='intimite-conjugale', category='couple', title='Intimité Conjugale',
                 short_description="Formation délicate sur l'intimité physique, émotionnelle et spirituelle.",
                 duration_label='3 semaines', sessions_label='6 sessions', audience='Couples mariés',
                 mode=Formation.Mode.PRESENTIEL, price=35000),
            dict(slug='finances-couples', category='preparation', title='Finances pour Couples',
                 short_description="Maîtrisez la gestion financière à deux.",
                 duration_label='5 semaines', sessions_label='10 modules', audience='Tous couples',
                 mode=Formation.Mode.HYBRIDE, price=45000, is_featured=True),
        ]

        for i, data in enumerate(formations_data):
            category = categories[data.pop('category')]
            slug = data.pop('slug')
            formation, _created = Formation.objects.update_or_create(
                slug=slug, defaults={**data, 'category': category, 'order': i, 'description': data['short_description']}
            )
            if not formation.highlights.exists():
                FormationHighlight.objects.create(formation=formation, icon='fa-check', title='Contenu complet', order=1)
            if not formation.sessions.exists():
                Session.objects.create(formation=formation, start_date=timezone.now().date() + timedelta(days=30), capacity=20)

    def seed_content(self):
        cat_comm, _ = ArticleCategory.objects.get_or_create(slug='communication', defaults={'name': 'Communication', 'badge_class': 'bg-info text-dark'})
        cat_fin, _ = ArticleCategory.objects.get_or_create(slug='finances', defaults={'name': 'Finances', 'badge_class': 'bg-warning text-dark'})
        cat_spi, _ = ArticleCategory.objects.get_or_create(slug='spiritualite', defaults={'name': 'Spiritualité', 'badge_class': 'bg-success text-white'})

        articles = [
            ('5-cles-desamorcer-conflits', cat_comm, 'Pasteur Daniel M.', '5 clés pour désamorcer les conflits dans le couple',
             "Découvrez comment transformer les désaccords en opportunités de croissance et d'écoute mutuelle."),
            ('argent-menage-serviteur-maitre', cat_fin, 'Équipe EDMAH', "L'argent dans le ménage : Serviteur ou Maître ?",
             "Des conseils pratiques pour gérer le budget familial avec transparence et sérénité."),
            ('construire-autel-familial', cat_spi, 'Marie K.', 'Construire un autel familial béni',
             "Comment mettre la prière au cœur de votre foyer et transmettre la foi aux enfants."),
        ]
        for i, (slug, category, author, title, excerpt) in enumerate(articles):
            Article.objects.update_or_create(
                slug=slug,
                defaults=dict(title=title, category=category, author_name=author, excerpt=excerpt,
                               body=excerpt, published_at=timezone.now() - timedelta(days=i * 8)),
            )

        gallery = [
            ('Cérémonie de Remise des Diplômes', 'Promotion 2024 - Yaoundé', 'evenements'),
            ('Retraite des Couples', 'Session de Kribi', 'evenements'),
            ('Atelier Communication', 'Session Pratique', 'temoignages'),
        ]
        for i, (title, subtitle, category) in enumerate(gallery):
            GalleryItem.objects.get_or_create(title=title, defaults=dict(subtitle=subtitle, category=category, order=i))

        faqs = [
            ("Comment s'inscrire à une formation ?", "Rendez-vous sur la page Inscriptions, choisissez votre formation et suivez les 4 étapes du formulaire."),
            ('Quels sont les moyens de paiement acceptés ?', "Le paiement est actuellement traité manuellement après validation du dossier ; notre équipe vous contactera."),
        ]
        for i, (q, a) in enumerate(faqs):
            FAQ.objects.get_or_create(question=q, defaults=dict(answer=a, order=i))

    def seed_events(self):
        events = [
            dict(slug='retraite-couples-2026', title='Grande Retraite des Couples 2026',
                 event_type=Event.EventType.PRESENTIEL,
                 description="Un week-end d'immersion totale dédié au ressourcement conjugal.",
                 start_datetime=timezone.now() + timedelta(days=60), location='Centre d\'Accompagnement, Yaoundé', capacity=80),
            dict(slug='atelier-budget-a-deux', title='Atelier : Gérer le Budget à Deux',
                 event_type=Event.EventType.WEBINAIRE,
                 description="Un atelier interactif d'1h30 pour une gestion saine des finances familiales.",
                 start_datetime=timezone.now() + timedelta(days=20), location='En ligne (Zoom)', capacity=200),
        ]
        for data in events:
            slug = data.pop('slug')
            Event.objects.update_or_create(slug=slug, defaults=data)

    def seed_learning(self):
        formation = Formation.objects.filter(slug='preparation').first()
        if not formation:
            return
        course, _ = Course.objects.get_or_create(formation=formation)

        modules_data = [
            ('Introduction', "Présentation du programme et des objectifs."),
            ('Communication', "Les bases d'une communication saine dans le couple."),
            ('Finances de Couple', "Gestion financière et budget familial."),
        ]
        for i, (title, description) in enumerate(modules_data, start=1):
            module, _ = Module.objects.get_or_create(
                course=course, order=i,
                defaults=dict(title=title, description=description, duration_label='45 min'),
            )
            quiz, _ = Quiz.objects.get_or_create(module=module, defaults={'pass_threshold': 80})
            if not quiz.questions.exists():
                question = Question.objects.create(quiz=quiz, order=1, text=f"Question de validation — {title}")
                Choice.objects.create(question=question, text='Bonne réponse', is_correct=True)
                Choice.objects.create(question=question, text='Mauvaise réponse', is_correct=False)

        demo_user, created = User.objects.get_or_create(
            username='apprenant.demo',
            defaults=dict(email='apprenant.demo@edmah.com', role=User.Role.APPRENANT, first_name='Marie', last_name='K.'),
        )
        if created:
            demo_user.set_password('EdmahDemo2026!')
            demo_user.save()

        Inscription.objects.get_or_create(
            user=demo_user, formation=formation, email=demo_user.email,
            defaults=dict(
                last_name='K.', first_name='Marie', birth_date='1995-01-01', gender='F',
                phone='+237600000000', marital_status=Inscription.MaritalStatus.FIANCE,
                address='Yaoundé, Cameroun', mode=Inscription.Mode.PRESENTIEL,
                status=Inscription.Status.ACCEPTE, id_photo='formations/placeholder.jpg',
                civil_document='formations/placeholder.jpg',
            ),
        )

        first_module = course.modules.order_by('order').first()
        if first_module:
            Progress.objects.get_or_create(user=demo_user, module=first_module, defaults={'completed': True, 'completed_at': timezone.now()})
