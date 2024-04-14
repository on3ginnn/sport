import django.apps
from django.utils.translation import gettext_lazy as _


__all__ = []


class HomepageConfig(django.apps.AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "homepage"
    verbose_name = _("homepage_app")
