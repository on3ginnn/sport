import django.contrib.auth.forms

import users.models

__all__ = []


def custom_auth_form(form):
    class CustomForm(form):
        def __init__(self, *args, **kwargs) -> None:
            super().__init__(*args, **kwargs)
            self.label_suffix = ""
            for field in self.visible_fields():
                field.field.widget.attrs["class"] = "form__input"

    return CustomForm


class SignUpForm(django.contrib.auth.forms.UserCreationForm):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.label_suffix = ""
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form__input"

    class Meta(django.contrib.auth.forms.UserCreationForm.Meta):
        model = users.models.User
        fields = (
            model.username.field.name,
            model.email.field.name,
        )


class ProfileEditForm(django.contrib.auth.forms.UserChangeForm):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.label_suffix = ""
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form__input"

        self.fields["avatar"].widget.attrs["class"] = "form__input input_file"

    class Meta(django.contrib.auth.forms.UserChangeForm.Meta):
        model = users.models.User
        fields = [
            users.models.User.avatar.field.name,
            users.models.User.username.field.name,
            users.models.User.first_name.field.name,
            users.models.User.last_name.field.name,
            users.models.User.birthday.field.name,
            users.models.User.bio.field.name,
            users.models.User.tg_link.field.name,
        ]
