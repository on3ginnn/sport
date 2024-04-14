import django.apps
from django.utils.translation import gettext_lazy as _

__all__ = []


class FeedbackConfig(django.apps.AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "feedback"
    verbose_name = _("feedback_app")
