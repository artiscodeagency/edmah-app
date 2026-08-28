import base64
import json

from django.core import mail
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase
from django.urls import reverse

from accounts.models import User
from catalog.models import Category, Formation
from events.models import Event, EventRegistration
from learning.models import Choice, Course, Module, Progress, Question, Quiz

PNG_1PX = base64.b64decode(
    b'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+A8AAQUBAScY42YAAAAASUVORK5CYII='
)


class InscriptionFlowTests(TestCase):
    def setUp(self):
        category = Category.objects.create(name='Préparation', slug='preparation')
        self.formation = Formation.objects.create(
            slug='preparation', category=category, title='Préparation au Mariage',
            short_description='desc', duration_label='8 semaines', price=50000,
        )

    def _post_registration(self, **overrides):
        payload = {
            'lastName': 'Kamdem', 'firstName': 'Paul', 'birthDate': '1990-01-01', 'gender': 'M',
            'email': 'paul@example.com', 'phone': '+237600000001', 'maritalStatus': 'celibataire',
            'address': 'Yaoundé', 'formation': 'preparation', 'mode': 'presentiel', 'motivations': '',
            'idPhoto': SimpleUploadedFile('photo.png', PNG_1PX, content_type='image/png'),
            'civilDocument': SimpleUploadedFile('civil.pdf', b'%PDF-1.4 x', content_type='application/pdf'),
        }
        payload.update(overrides)
        return self.client.post(reverse('inscription_submit'), data=payload)

    def test_valid_registration_creates_inscription_and_sends_emails(self):
        response = self._post_registration()
        self.assertEqual(response.status_code, 201)
        self.assertEqual(len(mail.outbox), 2)  # candidate + admin notification

    def test_registration_rejects_unknown_formation(self):
        response = self._post_registration(formation='does-not-exist')
        self.assertEqual(response.status_code, 400)

    def test_registration_rejects_missing_required_field(self):
        response = self._post_registration(email='')
        self.assertEqual(response.status_code, 400)

    def test_private_documents_are_not_publicly_reachable(self):
        self._post_registration()
        from .models import Inscription
        inscription = Inscription.objects.get(email='paul@example.com')

        # Not served by the public /media/ route.
        public_url = f'/media/{inscription.id_photo.name}'
        self.assertEqual(self.client.get(public_url).status_code, 404)

        # Anonymous users cannot fetch it through the protected view either.
        self.assertNotEqual(self.client.get(inscription.id_photo.url).status_code, 200)

        # Staff can.
        staff = User.objects.create_user('staffuser', password='pass1234', is_staff=True)
        self.client.force_login(staff)
        self.assertEqual(self.client.get(inscription.id_photo.url).status_code, 200)


class EventRegistrationTests(TestCase):
    def setUp(self):
        self.event = Event.objects.create(
            slug='atelier', title='Atelier', description='desc',
            start_datetime='2026-12-01T10:00:00Z', capacity=1,
        )

    def test_registration_and_duplicate_is_idempotent(self):
        url = reverse('event_register', args=[self.event.slug])
        payload = json.dumps({'full_name': 'Alice', 'email': 'alice@example.com'})
        response = self.client.post(url, data=payload, content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(EventRegistration.objects.count(), 1)

        response = self.client.post(url, data=payload, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(EventRegistration.objects.count(), 1)


class LearningAccessAndQuizTests(TestCase):
    def setUp(self):
        category = Category.objects.create(name='Préparation', slug='preparation')
        self.formation = Formation.objects.create(
            slug='preparation', category=category, title='Préparation au Mariage',
            short_description='desc', duration_label='8 semaines', price=50000,
        )
        self.course = Course.objects.create(formation=self.formation)
        self.module = Module.objects.create(course=self.course, order=1, title='Module 1')
        self.quiz = Quiz.objects.create(module=self.module, pass_threshold=80)
        self.question = Question.objects.create(quiz=self.quiz, order=1, text='Q1')
        self.correct = Choice.objects.create(question=self.question, text='Bon', is_correct=True)
        Choice.objects.create(question=self.question, text='Mauvais', is_correct=False)

        self.user = User.objects.create_user('apprenant1', password='pass1234', role=User.Role.APPRENANT)

    def test_unenrolled_user_is_redirected_away_from_course(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('course_detail', args=[self.formation.slug]))
        self.assertEqual(response.status_code, 302)

    def test_quiz_pass_marks_progress_completed(self):
        from admissions.models import Inscription
        Inscription.objects.create(
            user=self.user, formation=self.formation, email='apprenant1@example.com',
            last_name='X', first_name='Y', birth_date='1990-01-01', gender='M',
            phone='+237600000000', marital_status='celibataire', address='Yaoundé',
            mode='presentiel', status=Inscription.Status.ACCEPTE,
            id_photo='x.jpg', civil_document='x.jpg',
        )
        self.client.force_login(self.user)

        url = reverse('submit_quiz', args=[self.module.id])
        payload = json.dumps({str(self.question.id): self.correct.id})
        response = self.client.post(url, data=payload, content_type='application/json')

        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertTrue(body['passed'])
        self.assertEqual(body['score'], 100)
        self.assertTrue(Progress.objects.filter(user=self.user, module=self.module, completed=True).exists())

    def test_quiz_fail_does_not_mark_progress(self):
        from admissions.models import Inscription
        wrong_choice = self.question.choices.filter(is_correct=False).first()
        Inscription.objects.create(
            user=self.user, formation=self.formation, email='apprenant1@example.com',
            last_name='X', first_name='Y', birth_date='1990-01-01', gender='M',
            phone='+237600000000', marital_status='celibataire', address='Yaoundé',
            mode='presentiel', status=Inscription.Status.ACCEPTE,
            id_photo='x.jpg', civil_document='x.jpg',
        )
        self.client.force_login(self.user)

        url = reverse('submit_quiz', args=[self.module.id])
        payload = json.dumps({str(self.question.id): wrong_choice.id})
        response = self.client.post(url, data=payload, content_type='application/json')

        self.assertFalse(response.json()['passed'])
        self.assertFalse(Progress.objects.filter(user=self.user, module=self.module, completed=True).exists())
