import re

from django.core.exceptions import ValidationError
import django.utils.timezone
from django.utils.translation import gettext as _

__all__ = []


def birthday_validator(value):
    max_date = django.utils.timezone.now().date()
    if value > max_date:
        raise ValidationError(_("birthday_validation_error"))


def tg_link_validator(value):
    pattern = r"^(t|telegram)\.me\/[a-z0-9_]{5,32}"
    if re.search(pattern, value, re.IGNORECASE) is None:
        raise ValidationError(_("tg_link_validation_error"))


def inst_link_validator(value):
    pattern = r"^instagram\.com\/[a-z0-9-_]{1,255}"
    if re.search(pattern, value) is None:
        raise ValidationError(_("inst_link_validation_error"))
