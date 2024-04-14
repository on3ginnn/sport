__all__ = []

import django.apps
from django.utils.translation import gettext_lazy as _


class StreetsportConfig(django.apps.AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "streetsport"
    verbose_name = _("streetsport_app")
