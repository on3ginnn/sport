from django.contrib.auth.forms import UserCreationForm

import users.models

__all__ = []


def custom_auth_form(form):
    class CustomForm(form):
        def __init__(self, *args, **kwargs) -> None:
            super().__init__(*args, **kwargs)
            for field in self.visible_fields():
                field.field.widget.attrs["class"] = "form-control"

    return CustomForm


class SignUpForm(UserCreationForm):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"

    class Meta(UserCreationForm.Meta):
        model = users.models.User
        fields = (
            model.username.field.name,
            model.email.field.name,
        )
