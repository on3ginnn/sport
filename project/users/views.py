from django.conf import settings
import django.contrib
from django.contrib.auth import login
from django.core import signing
from django.core.mail import send_mail
import django.forms
from django.http import Http404
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
import django.views.generic

import users.forms
import users.models


__all__ = []


class SignupFormView(django.views.generic.FormView):
    form_class = users.forms.SignUpForm
    template_name = "users/signup.html"
    success_url = reverse_lazy("users:login")

    def form_valid(self, form):
        user = form.save(commit=False)
        if settings.DEFAULT_USER_IS_ACTIVE:
            user.is_active = True
            user.save()
            login(self.request, user)
            return super().form_valid(form)

        token = signing.dumps(form.cleaned_data)

        send_mail(
            subject="Activate your account",
            message=render_to_string(
                "users/signup_email.html", {"token": token}
            ),
            from_email=settings.EMAIL_ADMIN,
            recipient_list=[user.email],
        )
        django.contrib.messages.success(
            self.request,
            _("message_signup_success"),
        )
        return super().form_valid(form)


class ActivateRedirectView(django.views.generic.RedirectView):
    url = reverse_lazy("homepage:main")

    def get_redirect_url(self, *args, **kwargs):
        try:
            data = signing.loads(kwargs.get("username"))
        except signing.BadSignature:
            raise Http404

        users.forms.SignUpForm(data).save()
        django.contrib.messages.success(
            self.request,
            _("message_activate_success"),
        )

        return super().get_redirect_url(*args, **kwargs)
