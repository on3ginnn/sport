import django.conf
import django.db.models
import django.template.defaultfilters
from django.utils.translation import gettext as _


__all__ = []


class Status(django.db.models.TextChoices):
    NEW = "NW", _("new_status")
    PENDING = "PD", _("pending_status")
    COMPLETE = "CP", _("complete_status")


class Feedback(django.db.models.Model):
    text = django.db.models.TextField(
        _("text"),
        max_length=4000,
        help_text=_("text_field_help"),
    )
    created_on = django.db.models.DateTimeField(
        _("created"),
        help_text=_("created_field_help"),
        auto_now_add=True,
        null=True,
    )
    status = django.db.models.CharField(
        _("status"),
        choices=Status.choices,
        help_text=_("status_field_help"),
        default=Status.NEW,
        max_length=2,
    )

    @property
    def short_text(self):
        return django.template.defaultfilters.truncatechars(self.text, 100)

    short_text.fget.field_name = "short_text"
    short_text.fget.short_description = _("short_text")

    class Meta:
        verbose_name = _("feedback")
        verbose_name_plural = _("feedbacks")

    def __str__(self) -> str:
        return f"обратная связь ({self.id})"


class StatusLog(django.db.models.Model):
    user = django.db.models.ForeignKey(
        django.conf.settings.AUTH_USER_MODEL,
        help_text=_("user_field_help"),
        verbose_name=_("user"),
        on_delete=django.db.models.SET_NULL,
        null=True,
    )
    feedback = django.db.models.ForeignKey(
        Feedback,
        verbose_name=_("feedback"),
        help_text=_("feedback_field_help"),
        on_delete=django.db.models.SET_NULL,
        null=True,
    )
    timestamp = django.db.models.DateTimeField(
        _("timestamp"),
        help_text=_("timestamp_field_help"),
        auto_now_add=True,
        null=True,
    )
    from_status = django.db.models.CharField(
        _("from_status"),
        choices=Status.choices,
        help_text=_("from_status_field_help"),
        db_column="from",
        max_length=2,
    )
    to_status = django.db.models.CharField(
        _("to_status"),
        help_text=_("to_status_field_help"),
        choices=Status.choices,
        db_column="to",
        max_length=2,
    )

    class Meta:
        verbose_name = _("status_log")
        verbose_name_plural = _("status_logs")

    def __str__(self) -> str:
        return f"состояние ({self.id})"


class FeedbackFile(django.db.models.Model):
    def upload_to(self, filename):
        return f"uploads/{self.feedback_id}/{filename}"

    feedback = django.db.models.ForeignKey(
        Feedback,
        on_delete=django.db.models.CASCADE,
        verbose_name=_("feedback"),
        related_name="files",
        related_query_name="files",
        help_text=_("feedback_field_help"),
    )
    file = django.db.models.FileField(
        _("file"),
        upload_to=upload_to,
        help_text=_("file_field_help"),
    )

    class Meta:
        verbose_name = _("feedback_file")
        verbose_name_plural = _("feedback_files")


class FeedbackAuthor(django.db.models.Model):
    mail = django.db.models.EmailField(
        _("email address"),
        help_text=_("mail_field_help"),
    )
    feedback = django.db.models.OneToOneField(
        Feedback,
        on_delete=django.db.models.CASCADE,
        help_text=_("feedback_field_help"),
        verbose_name=_("feedback"),
        related_name="author",
        related_query_name="author",
    )

    class Meta:
        verbose_name = _("feedback_author")
        verbose_name_plural = _("feedback_authors")
