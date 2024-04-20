__all__ = []

import django.forms


class SearchForm(django.forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form__input"

    search_value = django.forms.CharField(
        max_length=254, label="поиск игрока или команды"
    )

    class Meta:
        fields = ["search_value"]
