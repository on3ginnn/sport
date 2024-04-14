import django.conf
import django.contrib.auth
import django.contrib.messages
import django.core.mail
import django.core.signing
import django.forms
import django.http
import django.template.loader
import django.urls
from django.utils.translation import gettext_lazy as _
import django.views.generic

import users.forms
import users.models


__all__ = []


class SignupFormView(django.views.generic.FormView):
    form_class = users.forms.SignUpForm
    template_name = "users/signup.html"
    success_url = django.urls.reverse_lazy("users:login")

    def form_valid(self, form):
        user = form.save(commit=False)
        if django.conf.settings.DEFAULT_USER_IS_ACTIVE:
            user.is_active = True
            user.save()
            django.contrib.auth.login(self.request, user)
            return super().form_valid(form)

        token = django.core.signing.dumps(form.cleaned_data)

        django.core.mail.send_mail(
            subject="Activate your account",
            message=django.template.loader.render_to_string(
                "users/signup_email.html",
                {"token": token},
            ),
            from_email=django.conf.settings.EMAIL_ADMIN,
            recipient_list=[user.email],
        )
        django.contrib.messages.success(
            self.request,
            _("message_signup_success"),
        )
        return super().form_valid(form)


class ActivateRedirectView(django.views.generic.RedirectView):
    django.views.generic.TemplateView
    url = django.urls.reverse_lazy("homepage:main")
    template_name = "users/signup.html"

    def get_redirect_url(self, *args, **kwargs):
        try:
            data = django.core.signing.loads(kwargs.get("token"))
        except django.core.signing.BadSignature:
            raise django.http.Http404

        form = users.forms.SignUpForm(data)
        if not form.is_valid():
            django.contrib.messages.success(
                self.request,
                _("message_activate_error"),
            )
            return super().get_redirect_url(*args, **kwargs)

        user = form.save()
        django.contrib.auth.login(self.request, user)
        django.contrib.messages.success(
            self.request,
            _("message_activate_success"),
        )

        return super().get_redirect_url(*args, **kwargs)
