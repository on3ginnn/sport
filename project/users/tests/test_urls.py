from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse

import users.models

__all__ = []


class StaticURLTests(TestCase):
    @classmethod
    def tearDownClass(cls):
        users.models.User.objects.all().delete()
        super().tearDownClass()

    def test_login_endpoint(self):
        status_code = self.client.get(reverse("users:login")).status_code
        self.assertEqual(status_code, HTTPStatus.OK)

    def test_signup_endpoint(self):
        status_code = self.client.get(reverse("users:signup")).status_code
        self.assertEqual(status_code, HTTPStatus.OK)

    def test_password_reset_endpoint(self):
        status_code = self.client.get(
            reverse("users:password_reset")
        ).status_code
        self.assertEqual(status_code, HTTPStatus.OK)

    def test_password_change_endpoint(self):
        status_code = self.client.get(
            reverse("users:password_reset")
        ).status_code
        self.assertEqual(status_code, HTTPStatus.OK)

    def test_password_reset_done_endpoint(self):
        status_code = self.client.get(
            reverse("users:password_reset_done")
        ).status_code
        self.assertEqual(status_code, HTTPStatus.OK)

    def test_password_change_done_endpoint(self):
        users.models.User.objects.create_user(username="test", password="test")
        response = self.client.post(
            reverse("users:login"),
            data={
                "username": "test",
                "password": "test",
            },
        )
        self.assertRedirects(
            response,
            reverse("homepage:main"),
            target_status_code=HTTPStatus.OK,
        )
        status_code = self.client.get(
            reverse("users:password_change_done")
        ).status_code
        self.assertEqual(status_code, HTTPStatus.OK)
