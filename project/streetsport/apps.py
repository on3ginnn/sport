__all__ = []

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class StreetsportConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "streetsport"
    verbose_name = _("streetsport app")
