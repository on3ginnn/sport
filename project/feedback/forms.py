from betterforms.multiform import MultiModelForm
import django.forms

import feedback.models

__all__ = []


class AbstractBaseForm(django.forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form__input"


class FeedbackForm(AbstractBaseForm):

    class Meta:
        model = feedback.models.Feedback
        exclude = [
            model.created_on.field.name,
            model.status.field.name,
        ]


class FeedbackAuthorForm(AbstractBaseForm):

    class Meta:
        model = feedback.models.FeedbackAuthor
        exclude = [
            model.feedback.field.name,
        ]


class MultipleFileInput(django.forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(django.forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            return [single_file_clean(d, initial) for d in data]

        return single_file_clean(data, initial)


class FeedbackFileForm(django.forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form__input input_file"

    files = MultipleFileField(required=False, label="Файлы")


class FeedbackMultiForm(MultiModelForm):
    form_classes = {
        "content": FeedbackForm,
        "author": FeedbackAuthorForm,
        "files": FeedbackFileForm,
    }
