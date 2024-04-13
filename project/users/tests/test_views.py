from http import HTTPStatus
from pathlib import Path
import shutil

from django.conf import settings
from django.core import signing
import django.core.mail
import django.test
import django.urls
import django.utils

import users.models

TEST_EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
TEST_EMAIL_FILE_PATH = settings.BASE_DIR / "send_mail"

__all__ = []


class TestUserViews(django.test.TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user_model = users.models.User

    @classmethod
    def tearDownClass(cls):
        if Path(TEST_EMAIL_FILE_PATH).exists():
            shutil.rmtree(TEST_EMAIL_FILE_PATH)

        cls.user_model.objects.all().delete()
        super().tearDownClass()

    @django.test.override_settings(DEFAULT_USER_IS_ACTIVE=True)
    def test_default_active_true_signup(self):
        data = {
            "username": "testinguser",
            "email": "testuser@example.com",
            "password1": "testpassword",
            "password2": "testpassword",
        }

        response = self.client.post(
            django.urls.reverse("users:signup"),
            data,
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            django.urls.reverse("users:login"),
        )

        self.assertTrue(
            self.user_model.objects.filter(username="testinguser").exists(),
        )

        user = django.shortcuts.get_object_or_404(
            django.contrib.auth.get_user_model().objects,
            username="testinguser",
        )

        self.assertTrue(
            user.is_authenticated,
        )

    @django.test.override_settings(
        DEFAULT_USER_IS_ACTIVE=False,
        EMAIL_BACKEND=TEST_EMAIL_BACKEND,
        EMAIL_FILE_PATH=TEST_EMAIL_FILE_PATH,
    )
    def test_default_active_false_signup(self):
        data = {
            "username": "testinguser",
            "email": "testuser@example.com",
            "password1": "testpassword",
            "password2": "testpassword",
        }

        response = self.client.post(
            django.urls.reverse("users:signup"),
            data,
        )
        self.assertEqual(response.status_code, 302)
        token = signing.dumps(data)
        self.assertTrue(Path(TEST_EMAIL_FILE_PATH).exists())
        with Path.open(next(Path(TEST_EMAIL_FILE_PATH).glob("*.log"))) as f:
            self.assertIn(token, f.read())

        response = self.client.get(
            django.urls.reverse("users:activate", args=[token])
        )
        self.assertRedirects(
            response,
            django.urls.reverse("homepage:main"),
            target_status_code=HTTPStatus.OK,
        )
        self.assertTrue(
            self.user_model.objects.filter(username="testinguser").exists(),
        )

        user = django.shortcuts.get_object_or_404(
            django.contrib.auth.get_user_model().objects,
            username="testinguser",
        )

        self.assertTrue(
            user.is_authenticated,
        )

    @django.test.override_settings(DEFAULT_USER_IS_ACTIVE=True)
    def test_login(self):
        data = {
            "username": "testinguser",
            "email": "testuser@example.com",
            "password1": "testpassword",
            "password2": "testpassword",
        }
        token = signing.dumps(data)
        self.client.get(django.urls.reverse("users:activate", args=[token]))
        response = self.client.post(
            django.urls.reverse("users:login"),
            {
                "username": data["username"],
                "password": data["password1"],
            },
        )
        self.assertRedirects(
            response,
            django.urls.reverse("homepage:main"),
        )
