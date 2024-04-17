import http

import django.test
import django.urls

__all__ = []


class StaticURLTests(django.test.TestCase):
    def test_about_endpoint(self):
        status_code = self.client.get(
            django.urls.reverse("homepage:main"),
        ).status_code
        self.assertEqual(status_code, http.HTTPStatus.OK)
