import pathlib
import uuid

import django.contrib.auth.models
import django.db.models
from django.utils.translation import gettext_lazy as _
import sorl.thumbnail

import users.validators

__all__ = []


class UserManager(django.contrib.auth.models.UserManager):
    CONONICAL_DOMAINS = {
        "yandex.ru": "ya.ru",
    }
    DOTS = {
        "ya.ry": "-",
        "gmail.com": "",
    }

    @classmethod
    def normalize_email(cls, email):
        email = super().normalize_email(email).lower()
        try:
            email_name, domain_part = email.rsplit("@", 1)
            email_name, *_ = email_name.split("+", 1)
            domain_part = cls.CONONICAL_DOMAINS.get(domain_part, domain_part)
            email_name = email_name.replace(
                ".",
                cls.DOTS.get(domain_part, "."),
            )
        except ValueError:
            pass
        else:
            email = f"{email_name}@{domain_part}"

        return email

    def by_mail(self, email):
        return self.get_queryset().get(email=self.normalize_email(email))

    def search_by_username(self, username):
        return (
            self.get_queryset()
            .filter(
                username__unaccent__icontains=username,
            )
            .order_by(User.username.field.name)
        )


class User(django.contrib.auth.models.AbstractUser):
    def get_path_image(self, filename):
        ext = pathlib.Path(filename).suffix
        return f"users/{self.id}/avatar{ext}"

    objects = UserManager()

    username = django.db.models.CharField(
        _("username"),
        max_length=32,
        unique=True,
        help_text=_("username_field_help"),
        validators=[
            users.validators.UsernameValidator(),
        ],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )

    email = django.db.models.EmailField(
        _("email address"),
        blank=True,
        unique=True,
    )

    bio = django.db.models.TextField(
        _("biography"),
        max_length=4000,
        help_text=_("bio_field_help"),
        blank=True,
        null=True,
    )
    birthday = django.db.models.DateField(
        _("birthday"),
        help_text=_("birthday_field_help"),
        validators=[users.validators.birthday_validator],
        null=True,
        blank=True,
    )
    avatar = sorl.thumbnail.ImageField(
        _("avatar"),
        help_text=_("avatar_field_help"),
        upload_to=get_path_image,
        null=True,
        blank=True,
    )
    tg_link = django.db.models.CharField(
        _("tg_link"),
        validators=[users.validators.TgLinkValidator()],
        help_text=_("tg_link_field_help"),
        max_length=44,
        blank=True,
        null=True,
    )
    rating = django.db.models.PositiveSmallIntegerField(
        _("rating"),
        help_text=_("rating_field_help"),
        default=0,
    )

    def get_image_preview_x100(self, obj=None):
        return sorl.thumbnail.get_thumbnail(
            obj or self.avatar,
            "100x100",
            crop="center",
            quality=51,
        )

    class Meta(django.contrib.auth.models.AbstractUser.Meta):
        swappable = "AUTH_USER_MODEL"


class Image(django.db.models.Model):
    def get_path_image(self, filename):
        ext = pathlib.Path(filename).suffix
        return f"users/{self.user_id}/{uuid.uuid4()}{ext}"

    user = django.db.models.ForeignKey(
        User,
        on_delete=django.db.models.CASCADE,
        verbose_name=_("user"),
        help_text=_("user_field_help"),
        related_name="images",
        related_query_name="images",
    )
    image = sorl.thumbnail.ImageField(
        _("image"),
        upload_to=get_path_image,
        help_text=_("image_field_help"),
    )

    class Meta:
        verbose_name = _("user_image")
        verbose_name_plural = _("user_images")

    def __str__(self):
        return pathlib.Path(self.image.path).stem
