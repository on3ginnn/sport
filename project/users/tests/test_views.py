import http
import pathlib
import shutil

import django.conf
import django.core.mail
import django.core.signing
import django.test
import django.urls
import django.utils

import users.models

TEST_EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
TEST_EMAIL_FILE_PATH = django.conf.settings.BASE_DIR / "send_mail"

__all__ = []


class TestUserViews(django.test.TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user_model = users.models.User

    @classmethod
    def tearDownClass(cls):
        if pathlib.Path(TEST_EMAIL_FILE_PATH).exists():
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
        token = django.core.signing.dumps(data)
        self.assertTrue(pathlib.Path(TEST_EMAIL_FILE_PATH).exists())
        with pathlib.Path.open(
            next(pathlib.Path(TEST_EMAIL_FILE_PATH).glob("*.log")),
        ) as f:
            self.assertIn(token, f.read())

        response = self.client.get(
            django.urls.reverse("users:activate", args=[token]),
        )
        self.assertRedirects(
            response,
            django.urls.reverse("homepage:main"),
            target_status_code=http.HTTPStatus.OK,
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
        token = django.core.signing.dumps(data)
        self.client.get(django.urls.reverse("users:activate", args=[token]))
        response1 = self.client.post(
            django.urls.reverse("users:login"),
            {
                "username": data["username"],
                "password": data["password1"],
            },
        )
        self.assertRedirects(
            response1,
            django.urls.reverse("homepage:main"),
        )
        response2 = self.client.post(
            django.urls.reverse("users:login"),
            {
                "username": data["email"],
                "password": data["password1"],
            },
        )
        self.assertRedirects(
            response2,
            django.urls.reverse("homepage:main"),
        )
