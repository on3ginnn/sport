import django.apps
from django.utils.translation import gettext_lazy as _

__all__ = []


class AboutConfig(django.apps.AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "about"
    verbose_name = _("about_app")
