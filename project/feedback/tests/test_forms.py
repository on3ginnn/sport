import pathlib
import shutil

import django.conf
import django.core.files.uploadedfile
import django.core.validators
import django.test
import django.urls
import django.utils
from django.utils.translation import gettext as _
import parameterized.parameterized

import feedback.forms
import feedback.models


__all__ = []


MEDIA_TEST: pathlib.Path = django.conf.settings.BASE_DIR / "media_test"


class FormTests(django.test.TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.form = feedback.forms.FeedbackForm()
        cls.form_author = feedback.forms.FeedbackAuthorForm()

    def test_mail_label(self):
        mail_label = FormTests.form_author.fields["mail"].label
        self.assertEqual(mail_label, _("email address").capitalize())

    def test_text_label(self):
        text_label = FormTests.form.fields["text"].label
        self.assertEqual(text_label, _("text").capitalize())

    def test_mail_help_text(self):
        mail_help_text = FormTests.form_author.fields["mail"].help_text
        self.assertEqual(
            mail_help_text,
            _("mail_field_help"),
        )

    def test_text_help_text(self):
        text_help_text = FormTests.form.fields["text"].help_text
        self.assertEqual(text_help_text, _("text_field_help"))

    @parameterized.parameterized.expand(
        [
            ("content", feedback.forms.FeedbackForm),
            ("author", feedback.forms.FeedbackAuthorForm),
            ("files", feedback.forms.FeedbackFileForm),
        ],
    )
    def test_correct_context(
        self,
        form_name,
        form_type,
    ):
        with self.subTest(form_name=form_name, form_type=form_type):
            response = self.client.get(
                django.urls.reverse("feedback:feedback"),
            )
            self.assertIn("form", response.context)
            self.assertIn(form_name, response.context["form"].forms)
            form = response.context["form"][form_name]
            self.assertIsInstance(form, form_type)

    @parameterized.parameterized.expand(
        [
            (
                {
                    "content-text": "some text",
                    "author-mail": "test@test.com",
                },
            ),
            (
                {
                    "content-text": "some text",
                    "author-mail": "test@test.com",
                },
            ),
        ],
    )
    def test_from(self, data):
        with self.subTest(data=data):
            feedback_count = feedback.models.Feedback.objects.count()
            response = self.client.post(
                django.urls.reverse("feedback:feedback"),
                data=data,
                follow=True,
            )

            self.assertRedirects(
                response,
                django.urls.reverse("feedback:feedback"),
            )
            self.assertEqual(
                feedback.models.Feedback.objects.count(),
                feedback_count + 1,
                "Feedback not created",
            )
            self.assertTrue(
                feedback.models.Feedback.objects.filter(
                    author__mail=data["author-mail"],
                    text=data["content-text"],
                ).exists(),
                "Uncorrect feedback created",
            )

    def test_form_errors(self):
        data = {"content-text": "some text", "author-mail": "wrong email"}
        feedback_count = feedback.models.Feedback.objects.count()
        response = self.client.post(
            django.urls.reverse("feedback:feedback"),
            data=data,
            follow=True,
        )
        self.assertFormError(
            response,
            "form",
            "author-mail",
            django.core.validators.EmailValidator.message,
        )
        self.assertEqual(
            feedback.models.Feedback.objects.count(),
            feedback_count,
            "Feedback created while validation failed",
        )

    @django.test.override_settings(MEDIA_ROOT=MEDIA_TEST)
    def test_form_file_upload(self):
        content = "Test file content".encode()
        file_upload = django.core.files.uploadedfile.SimpleUploadedFile(
            "file.txt",
            content,
            content_type="text/plain",
        )
        data = {
            "content-text": "some text",
            "author-mail": "test@test.com",
            "files-files": [file_upload],
        }
        feedback_count = feedback.models.Feedback.objects.count()

        response = self.client.post(
            django.urls.reverse("feedback:feedback"),
            data=data,
            format="multipart",
            follow=True,
        )

        self.assertRedirects(
            response,
            django.urls.reverse("feedback:feedback"),
        )
        self.assertEqual(
            feedback.models.Feedback.objects.count(),
            feedback_count + 1,
            "Feedback not created",
        )
        feedbacks = feedback.models.Feedback.objects.filter(
            author__mail=data["author-mail"],
            text=data["content-text"],
        ).get()
        files = list(feedbacks.files.all())
        self.assertEqual(len(files), 1, "Wrong count of files created")
        with (MEDIA_TEST / files[0].file.name).open("rb") as f:
            self.assertEqual(f.read(), content, "Wrong file content")

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        if pathlib.Path.exists(MEDIA_TEST):
            shutil.rmtree(MEDIA_TEST)
