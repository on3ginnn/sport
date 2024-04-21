import django.contrib.auth.forms
import django.contrib.auth.views
import django.urls

import users.forms
import users.views

__all__ = []


app_name = "users"

urlpatterns = [
    django.urls.path(
        "profile/<int:pk>/",
        users.views.ProfileDetailView.as_view(),
        name="profile",
    ),
    # TODO: сделать доступ к профилю без pk, т.к после редактирования профиля должен быть редирект на профиль текущего
    django.urls.path(
        "profile/",
        users.views.ProfileDetailView.as_view(),
        name="profile-current",
    ),
    django.urls.path(
        "profile/edit/",
        users.views.ProfileEditFormView.as_view(),
        name="profile-edit",
    ),
    django.urls.path(
        "profile/delete/",
        users.views.UserDeleteView.as_view(),
        name="user-delete",
    ),
    django.urls.path(
        "login/",
        django.contrib.auth.views.LoginView.as_view(
            template_name="users/login.html",
            redirect_authenticated_user=True,
            authentication_form=users.forms.custom_auth_form(
                django.contrib.auth.forms.AuthenticationForm,
            ),
        ),
        name="login",
    ),
    django.urls.path(
        "logout/",
        django.contrib.auth.views.LogoutView.as_view(),
        name="logout",
    ),
    django.urls.path(
        "password_change/",
        django.contrib.auth.views.PasswordChangeView.as_view(
            template_name="users/password_change.html",
            form_class=users.forms.custom_auth_form(
                django.contrib.auth.forms.PasswordChangeForm,
            ),
        ),
        name="password_change",
    ),
    django.urls.path(
        "password_change/done/",
        django.contrib.auth.views.PasswordChangeDoneView.as_view(
            template_name="users/password_change_done.html",
        ),
        name="password_change_done",
    ),
    django.urls.path(
        "password_reset/",
        django.contrib.auth.views.PasswordResetView.as_view(
            template_name="users/password_reset.html",
            form_class=users.forms.custom_auth_form(
                django.contrib.auth.forms.PasswordResetForm,
            ),
            success_url=django.urls.reverse_lazy("users:password_reset_done"),
        ),
        name="password_reset",
    ),
    django.urls.path(
        "password_reset/done/",
        django.contrib.auth.views.PasswordResetDoneView.as_view(
            template_name="users/password_reset_done.html",
        ),
        name="password_reset_done",
    ),
    django.urls.path(
        "reset/<uidb64>/<token>/",
        django.contrib.auth.views.PasswordResetConfirmView.as_view(
            form_class=users.forms.custom_auth_form(
                django.contrib.auth.forms.SetPasswordForm,
            ),
            template_name="users/password_reset_confirm.html",
            success_url=django.urls.reverse_lazy(
                "users:password_reset_complete",
            ),
        ),
        name="password_reset_confirm",
    ),
    django.urls.path(
        "reset/done/",
        django.contrib.auth.views.PasswordResetCompleteView.as_view(
            template_name="users/password_reset_complete.html",
        ),
        name="password_reset_complete",
    ),
    django.urls.path(
        "signup/",
        users.views.SignupFormView.as_view(
            redirect_authenticated_user=True,
        ),
        name="signup",
    ),
    django.urls.path(
        "activate/<token>/",
        users.views.ActivateRedirectView.as_view(),
        name="activate",
    ),
]
