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
            username="test",
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
            (f"telegram.me/{'t' * 32}", True),
            ("telegram.me/testt", True),
            ("telegram.me/tesTT", True),
            ("t.me/test_", True),
            ("t.me/test", False),
            ("t.me/test@", False),
            ("telegram.me/test", False),
            (f"telegram.me/{'t' * 33}", False),
            ("t.me", False),
            ("telegram.me", False),
            ("test", False),
        ]
    )
    def test_tg_link_validator(self, tg_link, is_valid):
        count = users.models.User.objects.count()
        if is_valid:
            user = users.models.User(
                username="test",
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
            ("instagram.com/t", True),
            (f"instagram.com/{'t' * 255}", True),
            ("instagram.com/t-t-t__", True),
            ("instagram.com/t-t-__@", False),
            ("instagram.com/T", False),
            (f"instagram.com/{'t' * 256}", False),
        ]
    )
    def test_inst_link_validator(self, inst_link, is_valid):
        count = users.models.User.objects.count()
        if is_valid:
            user = users.models.User(
                username="test",
                password="test",
                inst_link=inst_link,
            )
            user.full_clean()
            user.save()
            self.assertEqual(
                users.models.User.objects.count(),
                count + 1,
                msg=f"no add validate by inst_link({inst_link}) user",
            )
        else:
            with self.assertRaises(ValidationError):
                user = users.models.User(
                    username="test",
                    password="test",
                    inst_link=inst_link,
                )
                user.full_clean()
                user.save()
                self.assertEqual(
                    users.models.User.objects.count(),
                    count,
                    msg=f"add no validate by inst_link({inst_link}) user",
                )
