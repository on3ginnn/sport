import pathlib
import re

import django.core.exceptions
import django.db.models
import django.middleware
from django.utils.translation import gettext as _
import slugify
import sorl.thumbnail

import streetsport.validators

__all__ = []


def normalize_str(value):
    words = re.findall("[0-9а-яёa-z]+", value.lower())
    return slugify.slugify("".join(words))


class Game(django.db.models.Model):
    def get_path_image(self, filename):
        ext = pathlib.Path(filename).suffix
        return f"streetsport/game/game_{self.id}{ext}"

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

    icon = sorl.thumbnail.ImageField(
        _("game_icon"),
        help_text=_("game_icon_field_help"),
        upload_to=get_path_image,
        null=True,
        blank=True,
    )

    def get_image_preview_x50(self, obj=None):
        return sorl.thumbnail.get_thumbnail(
            obj or self.icon,
            "50x50",
            crop="center",
            quality=51,
            format="PNG",
        )

    def clean(self):
        normalize_title = normalize_str(self.title)
        found = Game.objects.filter(
            ~django.db.models.Q(id=self.id),
            normalize_title=normalize_title,
        )
        if found.values("id"):
            raise django.core.exceptions.ValidationError(
                {Game.title.field.name: _("normalize_title_validation_error")},
            )

        self.normalize_title = normalize_title

    class Meta:
        verbose_name = _("game")
        verbose_name_plural = _("games")

    def __str__(self):
        return self.title


class TeamManager(django.db.models.Manager):
    def detail(self):
        return (
            self.get_queryset()
            .filter()
            .select_related(Team.game.field.name, Team.lead.related.name)
            .prefetch_related(
                django.db.models.Prefetch(
                    Team.teammates.field.related_query_name(),
                    queryset=Team.teammates.field.model.objects.only(
                        Team.teammates.field.model.id.field.name,
                        Team.teammates.field.model.username.field.name,
                        Team.teammates.field.model.avatar.field.name,
                        Team.teammates.field.model.rating.field.name,
                    ),
                )
            )
            .only(
                Team.id.field.name,
                Team.avatar.field.name,
                Team.rating.field.name,
                Team.title.field.name,
                f"{Team.game.field.name}__{Game.id.field.name}",
                f"{Team.game.field.name}__{Game.icon.field.name}",
                f"{Team.game.field.name}__{Game.title.field.name}",
                (
                    f"{Team.lead.related.name}"
                    f"__{Team.lead.related.model.id.field.name}"
                ),
                Team.teammates.field.related_query_name(),
            )
        )

    def delete_view(self):
        return (
            self.get_queryset()
            .filter()
            .select_related(Team.lead.related.name)
            .only(
                Team.id.field.name,
                (
                    f"{Team.lead.related.name}"
                    f"__{Team.lead.related.model.id.field.name}"
                ),
            )
        )

    def search_by_title(self, title):
        return (
            self.get_queryset()
            .filter(
                title__unaccent__icontains=title,
            )
            .order_by(Team.title.field.name)
        )


class Team(django.db.models.Model):
    def get_path_image(self, filename):
        ext = pathlib.Path(filename).suffix
        return f"streetsport/team_{self.id}{ext}"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    objects = TeamManager()

    title = django.db.models.CharField(
        _("title"),
        help_text=_("title_field_help"),
        max_length=50,
        unique=True,
    )
    avatar = sorl.thumbnail.ImageField(
        _("avatar"),
        help_text=_("avatar_field_help"),
        upload_to=get_path_image,
        null=True,
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
    rating = django.db.models.PositiveSmallIntegerField(
        _("rating"),
        help_text=_("rating_field_help"),
        default=0,
    )

    def get_image_preview_400x300(self, obj=None):
        return sorl.thumbnail.get_thumbnail(
            obj or self.avatar,
            "400x300",
            crop="center",
            quality=51,
        )

    def get_image_preview_x100(self, obj=None):
        return sorl.thumbnail.get_thumbnail(
            obj or self.avatar,
            "100x100",
            crop="center",
            quality=51,
        )

    def clean(self):
        normalize_title = normalize_str(self.title)
        found = Team.objects.filter(
            ~django.db.models.Q(id=self.id),
            normalize_title=normalize_title,
        )
        if found.values("id"):
            raise django.core.exceptions.ValidationError(
                {Team.title.field.name: _("normalize_title_validation_error")},
            )

        self.normalize_title = normalize_title

    @property
    def orders(self):
        return Order.objects.filter(
            django.db.models.Q(team_one=self)
            | django.db.models.Q(team_two=self),
        )

    class Meta:
        verbose_name = _("team")
        verbose_name_plural = _("teams")

    def __str__(self):
        return self.title


class OrderManager(django.db.models.Manager):
    def homepage(self):
        return (
            self.get_queryset()
            .select_related(
                Order.team_one.field.name,
                Order.team_two.field.name,
                Order.game.field.name,
                f"{Order.team_one.field.name}__{Team.lead.related.name}",
                f"{Order.team_two.field.name}__{Team.lead.related.name}",
            )
            .prefetch_related(
                django.db.models.Prefetch(
                    (
                        f"{Order.team_one.field.name}__"
                        f"{Team.teammates.field.related_query_name()}"
                    ),
                    queryset=Team.teammates.field.model.objects.order_by(
                        Team.teammates.field.model.rating.field.name,
                    ).only(Team.teammates.field.model.avatar.field.name),
                ),
                django.db.models.Prefetch(
                    (
                        f"{Order.team_two.field.name}__"
                        f"{Team.teammates.field.related_query_name()}"
                    ),
                    queryset=Team.teammates.field.model.objects.order_by(
                        Team.teammates.field.model.rating.field.name,
                    ).only(Team.teammates.field.model.avatar.field.name),
                ),
            )
            .order_by(f"-{Order.start.field.name}")[:10]
        ).only(
            Order.id.field.name,
            Order.start.field.name,
            f"{Order.game.field.name}__{Game.title.field.name}",
            f"{Order.game.field.name}__{Game.icon.field.name}",
            f"{Order.team_one.field.name}__{Team.title.field.name}",
            (
                f"{Order.team_one.field.name}"
                f"__{Team.teammates.field.related_query_name()}"
                f"__{Team.teammates.field.model.avatar.field.name}"
            ),
            (
                f"{Order.team_one.field.name}__{Team.lead.related.name}"
                f"__{Team.lead.related.model.avatar.field.name}"
            ),
            f"{Order.team_one.field.name}__{Team.avatar.field.name}",
            f"{Order.team_two.field.name}__{Team.title.field.name}",
            (
                f"{Order.team_two.field.name}"
                f"__{Team.teammates.field.related_query_name()}"
                f"__{Team.teammates.field.model.avatar.field.name}"
            ),
            (
                f"{Order.team_two.field.name}__{Team.lead.related.name}"
                f"__{Team.lead.related.model.avatar.field.name}"
            ),
            f"{Order.team_two.field.name}__{Team.avatar.field.name}",
        )


class Order(django.db.models.Model):
    objects = OrderManager()
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
        verbose_name=_("team_two"),
        help_text=_("team_one_field_help"),
        related_name="orders_two",
        related_query_name="orders_two",
    )
    game = django.db.models.ForeignKey(
        Game,
        on_delete=django.db.models.CASCADE,
        verbose_name=_("order_game"),
        help_text=_("order_game_help_text"),
        related_name="order_game",
        related_query_name="order_game",
        null=True,
        blank=False,
    )
    start = django.db.models.DateTimeField(
        _("start"),
        help_text=_("start_field_help"),
        validators=[streetsport.validators.start_validator],
        null=True,
        blank=True,
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
            raise django.core.exceptions.ValidationError(
                {Order.team_two.field.name: _("team_equal_validation_error")},
            )

    class Meta:
        verbose_name = _("order")
        verbose_name_plural = _("orders")

    def __str__(self):
        return f"{self.start}: {self.team_one} - {self.team_two}"
