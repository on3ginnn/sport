import re

from django.core.exceptions import ValidationError
import django.db
from django.utils.translation import gettext as _
from slugify import slugify

import users.models


__all__ = []


def normalize_str(value):
    words = re.findall("[0-9а-яёa-z]+", value.lower())
    return slugify("".join(words))


class Game(django.db.models.Model):
    title = django.db.models.CharField(
        _("title"),
        help_text=_("title_field_help"),
        unique=True,
        max_length=50,
    )
    normalize_title = django.db.models.CharField(
        _("normalize_title"),
        max_length=50,
        editable=False,
        help_text=_("normalize_title_field_help"),
    )

    def clean(self):
        normalize_title = normalize_str(self.title)
        found = Game.objects.filter(
            ~django.db.models.Q(id=self.id),
            normalize_title=normalize_title,
        )
        if found.values("id"):
            raise ValidationError(
                {Game.title.field.name: _("normalize_title_validation_error")},
            )

        self.normalize_title = normalize_title


class Team(django.db.models.Model):
    title = django.db.models.CharField(
        _("title"),
        help_text=_("title_field_help"),
        max_length=50,
        unique=True,
    )
    lead = django.db.models.ForeignKey(
        users.models.User,
        on_delete=django.db.models.CASCADE,
        verbose_name=_("lead"),
        help_text=_("lead_field_help"),
        related_name="lead_teams",
        related_query_name="lead_teams",
        blank=True,
        null=True,
    )
    teammates = django.db.models.ManyToManyField(
        users.models.User,
        verbose_name=_("teammates"),
        help_text=_("teammates_field_help"),
        related_name="teams",
        related_query_name="teams",
        blank=True,
    )
    game = django.db.models.ForeignKey(
        Game,
        on_delete=django.db.models.CASCADE,
        verbose_name=_("game"),
        help_text=_("game_field_help"),
        related_name="teams",
        related_query_name="teams",
        blank=True,
        null=True,
    )
    normalize_title = django.db.models.CharField(
        _("normalize_title"),
        max_length=50,
        editable=False,
        help_text=_("normalize_title_field_help"),
    )
    rating = django.db.models.PositiveIntegerField(
        _("rating"),
        help_text=_("rating_field_help"),
        default=0,
    )

    def clean(self):
        normalize_title = normalize_str(self.title)
        found = Team.objects.filter(
            ~django.db.models.Q(id=self.id),
            normalize_title=normalize_title,
        )
        if found.values("id"):
            raise ValidationError(
                {Team.title.field.name: _("normalize_title_validation_error")},
            )

        self.normalize_title = normalize_title

    @property
    def children(self):
        return Order.objects.filter(
            django.db.models.Q(team_one=self)
            | django.db.models.Q(team_two=self),
        )

    class Meta:
        verbose_name = _("team")
        verbose_name_plural = _("teams")


class Order(django.db.models.Model):
    team_one = django.db.models.ForeignKey(
        Team,
        on_delete=django.db.models.CASCADE,
        verbose_name=_("team_one"),
        help_text=_("team_one_field_help"),
        related_name="orders_one",
        related_query_name="orders_one",
    )
    team_two = django.db.models.ForeignKey(
        Team,
        on_delete=django.db.models.CASCADE,
        verbose_name=_("team_one"),
        help_text=_("team_one_field_help"),
        related_name="orders_two",
        related_query_name="orders_two",
    )
    description = django.db.models.TextField(
        _("description"),
        max_length=4000,
        help_text=_("description_field_help"),
        blank=True,
        null=True,
    )

    location = django.db.models.URLField(
        _("location"),
        max_length=255,
        help_text=_("location_field_help"),
        blank=True,
        null=True,
    )

    def clean(self):
        if self.team_one == self.team_two:
            raise ValidationError(
                {Order.team_two.field.name: _("team_equal_validation_error")},
            )
