import itertools

from django.core.exceptions import ValidationError
from django.test import TestCase
import parameterized

import streetsport.models
import users.models


__all__ = []


class DBNormalizetitleTests(TestCase):
    @classmethod
    def tearDownClass(cls):
        streetsport.models.Game.objects.all().delete()
        super().tearDownClass()

    @parameterized.parameterized.expand(
        (
            (test_value[0], *test_value[1])
            for test_value in itertools.product(
                [
                    ("test"),
                    ("Тest"),
                    ("tЕst"),
                ],
                [
                    ("test test", True),
                    ("itfaketest", True),
                    ("test, test", True),
                    ("test!test", True),
                    ("testt", True),
                    ("test!", False),
                    ("!test", False),
                    ("!test!", False),
                    (" test ", False),
                    ("test,", False),
                    (".test", False),
                    ("te st", False),
                    ("te sТ", False),
                    ("tеst", False),
                ],
            )
        ),
    )
    def test_add_game(self, title1, title2, is_validate):
        count = streetsport.models.Game.objects.count()
        self.game1 = streetsport.models.Game(
            title=title1,
        )
        self.game2 = streetsport.models.Game(
            title=title2,
        )
        if not is_validate:
            with self.assertRaises(ValidationError):
                self.game1.full_clean()
                self.game1.save()
                self.game2.full_clean()
                self.game2.save()

                self.assertEqual(
                    streetsport.models.Game.objects.count(),
                    count + 1,
                    msg=f"add {title2} but we have {title1}",
                )
        else:
            self.game1.full_clean()
            self.game1.save()
            self.game2.full_clean()
            self.game2.save()
            self.assertEqual(
                streetsport.models.Game.objects.count(),
                count + 2,
                msg=f"no add {title2} validate game but we have {title1}",
            )


class DBTeamTests(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.user = users.models.User.objects.create(
            username="test2",
            password="test",
        )
        cls.game = streetsport.models.Game.objects.create(
            title="test",
        )
        return super().setUpClass()

    def test_user_teams_game_not_equal(self):
        self.team1 = streetsport.models.Team(
            title="test1",
            game=self.game,
        )
        self.team1.full_clean()
        self.team1.save()

        self.team2 = streetsport.models.Team(
            title="test2",
            game=self.game,
        )
        self.team2.full_clean()
        self.team2.save()
        count = self.team2.teammates.count()

        self.team1.teammates.add(self.user)
        self.team1.full_clean()
        self.team1.save()
        with self.assertRaises(ValidationError):
            self.team2.teammates.add(self.user)
            self.team2.full_clean()
            self.team2.save()
            self.assertEqual(
                self.team2.teammates.count(),
                count,
                msg=f"add user in {self.team1} but we have {self.team2}",
            )

    @classmethod
    def tearDownClass(cls):
        users.models.User.objects.all().delete()
        streetsport.models.Team.objects.all().delete()
        streetsport.models.Game.objects.all().delete()
        super().tearDownClass()


class DBOrderTests(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.team1 = streetsport.models.Team.objects.create(
            title="test3",
        )
        return super().setUpClass()

    @classmethod
    def tearDownClass(cls):
        streetsport.models.Team.objects.all().delete()
        streetsport.models.Order.objects.all().delete()
        super().tearDownClass()

    def test_order_teams_not_equal(self):
        count = streetsport.models.Order.objects.count()
        self.order = streetsport.models.Order(
            team_one=self.team1,
            team_two=self.team1,
        )
        with self.assertRaises(ValidationError):
            self.order.full_clean()
            self.order.save()
            self.assertEqual(
                streetsport.models.Order.objects.count(),
                count,
                msg="add equal team in order",
            )
