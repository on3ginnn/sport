import re

from django.core import validators
from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
import django.utils.timezone
from django.utils.translation import gettext as _


__all__ = []


@deconstructible
class UsernameValidator(validators.RegexValidator):
    regex = r"^[\w_]{5,32}"
    message = _("username_validation_error")
    flags = re.ASCII


def birthday_validator(value):
    max_date = django.utils.timezone.now().date()
    if value > max_date:
        raise ValidationError(_("birthday_validation_error"))


@deconstructible
class TgLinkValidator(validators.RegexValidator):
    regex = r"^(t|telegram)\.me\/[a-z0-9_]{5,32}"
    message = _("tg_link_validation_error")
    flags = re.IGNORECASE
