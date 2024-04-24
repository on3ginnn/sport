import django.forms

import streetsport.models

__all__ = []


class StreetsportOrderModelForm(django.forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form__input"

        self.fields[streetsport.models.Order.team_one.field.name].disabled = (
            True
        )

    class Meta:
        model = streetsport.models.Order
        exclude = []


class TeamEditForm(django.forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form__input"

    class Meta:
        model = streetsport.models.Team
        exclude = [streetsport.models.Team.rating.field.name]
