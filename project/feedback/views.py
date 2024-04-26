import django.conf
import django.contrib.messages
import django.core.mail
import django.shortcuts
import django.urls
from django.utils.translation import gettext_lazy as _
import django.views.generic

import feedback.forms
import feedback.models

__all__ = []


class FeedbackCreateView(django.views.generic.CreateView):
    template_name = "feedback/feedback.html"
    form_class = feedback.forms.FeedbackMultiForm
    success_url = django.urls.reverse_lazy("feedback:feedback")

    def form_valid(self, form):
        author_form = form["author"]
        content_form = form["content"]
        files_form = form["files"]

        feedback_instance = content_form.save(commit=True)
        author_form.instance.feedback = feedback_instance
        author_form.save(commit=True)

        files = files_form.cleaned_data["files"]
        email_send = django.core.mail.EmailMessage(
            subject="Feedback",
            body=content_form.cleaned_data["text"],
            from_email=author_form.cleaned_data["mail"],
            to=[django.conf.settings.EMAIL_ADMIN],
        )
        for file in files:
            email_send.attach(file.name, file.file.read(), file.content_type)
            feedback.models.FeedbackFile(
                file=file,
                feedback=feedback_instance,
            ).save()

        email_send.send()

        django.contrib.messages.success(
            self.request,
            _("message_form_success"),
        )
        return django.shortcuts.redirect(self.success_url)
