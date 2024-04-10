from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
import django.views.generic

from feedback.forms import (
    FeedbackMultiForm,
)
from feedback.models import FeedbackFile
import feedback.tasks

__all__ = []


class FeedbackCreateView(django.views.generic.CreateView):
    template_name = "feedback/feedback.html"
    form_class = FeedbackMultiForm
    success_url = reverse_lazy("feedback:feedback")

    def form_valid(self, form):
        author_form = form["author"]
        content_form = form["content"]
        files_form = form["files"]

        feedback_instance = content_form.save(commit=True)
        author_form.instance.feedback = feedback_instance
        author_form.save(commit=True)

        files = files_form.cleaned_data["files"]
        for file in files:
            FeedbackFile(file=file, feedback=feedback_instance).save()

        feedback.tasks.send_feedback_email_task.delay(
            author_form.cleaned_data["mail"],
            content_form.cleaned_data["text"],
        )
        messages.success(self.request, _("message_form_success"))
        return redirect(self.success_url)
