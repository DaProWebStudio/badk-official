import shutil
import tempfile
from io import BytesIO

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse
from PIL import Image

from apps.feedback.models import FeedBack, Recaptcha
from apps.feedback.views import CAPTCHA_SESSION_KEY

MEDIA_ROOT = tempfile.mkdtemp()


def make_image():
    buf = BytesIO()
    Image.new('RGB', (350, 60), 'white').save(buf, format='PNG')
    return SimpleUploadedFile('captcha.png', buf.getvalue(), content_type='image/png')


@override_settings(MEDIA_ROOT=MEDIA_ROOT)
class ContactsCaptchaTests(TestCase):
    url = reverse('contacts')

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(MEDIA_ROOT, ignore_errors=True)

    def setUp(self):
        self.captchas = [Recaptcha.objects.create(image=make_image(), answer=answer) for answer in (12, 7, 30)]

    def data(self, answer):
        return {
            'name': 'Айбек',
            'email': 'test@example.com',
            'message': 'Сообщение длиной больше двадцати символов',
            'user_answer': answer,
        }

    def shown_captcha(self):
        return Recaptcha.objects.get(pk=self.client.session[CAPTCHA_SESSION_KEY])

    def test_correct_answer_saves_message(self):
        self.client.get(self.url)
        captcha = self.shown_captcha()

        response = self.client.post(self.url, self.data(captcha.answer))

        self.assertRedirects(response, self.url + '#feedback', fetch_redirect_response=False)
        self.assertEqual(FeedBack.objects.count(), 1)

    def test_answer_is_checked_against_shown_captcha(self):
        # Регрессия: раньше при POST выбиралась новая случайная капча
        self.client.get(self.url)
        captcha = self.shown_captcha()
        for _ in range(5):
            response = self.client.post(self.url, self.data(captcha.answer))
            self.assertEqual(response.status_code, 302)
            captcha = self.shown_captcha()
        self.assertEqual(FeedBack.objects.count(), 5)

    def test_wrong_answer_shows_error_and_rotates_captcha(self):
        self.client.get(self.url)
        captcha = self.shown_captcha()

        response = self.client.post(self.url, self.data(captcha.answer + 1))

        self.assertEqual(response.status_code, 200)
        self.assertFormError(response.context['form'], 'user_answer', 'Не правильный ответ')
        self.assertEqual(FeedBack.objects.count(), 0)
        self.assertNotEqual(self.shown_captcha().pk, captcha.pk)
        self.assertEqual(response.context['recaptcha'].pk, self.shown_captcha().pk)

    def test_post_without_session_is_rejected(self):
        response = self.client.post(self.url, self.data(12))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(FeedBack.objects.count(), 0)

    def test_page_works_without_captchas(self):
        Recaptcha.objects.all().delete()

        self.assertEqual(self.client.get(self.url).status_code, 200)
        data = self.data(0)
        del data['user_answer']
        self.client.post(self.url, data)

        self.assertEqual(FeedBack.objects.count(), 1)
