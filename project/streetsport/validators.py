import django.core.exceptions
import django.utils.timezone
from django.utils.translation import gettext as _

__all__ = []


def start_validator(value):
    max_date = django.utils.timezone.now()
    if value <= max_date:
        raise django.core.exceptions.ValidationError(
            _("start_validation_error"),
        )
