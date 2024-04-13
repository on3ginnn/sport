from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone
import parameterized

import users.models


__all__ = []


class DBUserTests(TestCase):
    @classmethod
    def tearDownClass(cls):
        users.models.User.objects.all().delete()
        super().tearDownClass()

    def test_birthday_validator(self):
        now = timezone.now().date()
        count = users.models.User.objects.count()
        with self.assertRaises(ValidationError):
            no_valid = now + timezone.timedelta(days=1)
            user = users.models.User(
                username="test",
                password="test",
                birthday=no_valid,
            )
            user.full_clean()
            user.save()
            self.assertEqual(
                users.models.User.objects.count(),
                count,
                msg=f"add no validate by birthday({no_valid}) user",
            )

        user = users.models.User(
            username="testt",
            password="test",
            birthday=now,
        )
        user.full_clean()
        user.save()
        self.assertEqual(
            users.models.User.objects.count(),
            count + 1,
            msg=f"no add validate by birthday({now}) user",
        )

    @parameterized.parameterized.expand(
        [
            ("t.me/testt", True),
            ("telegram.me/" + "t" * 32, True),
            ("telegram.me/testt", True),
            ("telegram.me/tesTT", True),
            ("t.me/test_", True),
            ("t.me/test", False),
            ("t.me/test@", False),
            ("telegram.me/test", False),
            ("telegram.me/" + "t" * 33, False),
            ("t.me", False),
            ("telegram.me", False),
            ("test", False),
        ]
    )
    def test_tg_link_validator(self, tg_link, is_valid):
        count = users.models.User.objects.count()
        if is_valid:
            user = users.models.User(
                username="testt",
                password="test",
                tg_link=tg_link,
            )
            user.full_clean()
            user.save()
            self.assertEqual(
                users.models.User.objects.count(),
                count + 1,
                msg=f"no add validate by tg_link({tg_link}) user",
            )
        else:
            with self.assertRaises(ValidationError):
                user = users.models.User(
                    username="test",
                    password="test",
                    tg_link=tg_link,
                )
                user.full_clean()
                user.save()
                self.assertEqual(
                    users.models.User.objects.count(),
                    count,
                    msg=f"add no validate by tg_link({tg_link}) user",
                )

    @parameterized.parameterized.expand(
        [
            ("testt", True),
            ("test_test", True),
            ("t" * 32, True),
            ("tesTT", True),
            ("T_T_T_T", True),
            ("test!", False),
            ("T__##3", False),
            ("@TT1T", False),
            ("t" * 33, False),
            ("test", False),
        ]
    )
    def test_username_validator(self, username, is_valid):
        count = users.models.User.objects.count()
        if is_valid:
            user = users.models.User(
                username=username,
                password="test",
            )
            user.full_clean()
            user.save()
            self.assertEqual(
                users.models.User.objects.count(),
                count + 1,
                msg=f"no add validate by username({username}) user",
            )
        else:
            with self.assertRaises(ValidationError):
                user = users.models.User(
                    username=username,
                    password="test",
                )
                user.full_clean()
                user.save()
                self.assertEqual(
                    users.models.User.objects.count(),
                    count,
                    msg=f"add no validate by username({username}) user",
                )

    def test_username_search(self):
        users_ls = []
        for i in range(10):
            user = users.models.User.objects.create_user(
                username=f"test{i}",
                password="123",
                email=f"test{i}@example.com",
            )
            users_ls.append(user)

        self.assertQuerySetEqual(
            users_ls,
            users.models.User.objects.search_by_username("test"),
        )
