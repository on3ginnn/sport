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
        for file in files:
            feedback.models.FeedbackFile(
                file=file,
                feedback=feedback_instance,
            ).save()

        django.core.mail.send_mail(
            subject="Feedback",
            message=content_form.cleaned_data["text"],
            from_email=django.conf.settings.EMAIL_ADMIN,
            recipient_list=[author_form.cleaned_data["mail"]],
        )

        django.contrib.messages.success(
            self.request,
            _("message_form_success"),
        )
        return django.shortcuts.redirect(self.success_url)
