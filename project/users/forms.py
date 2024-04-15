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
