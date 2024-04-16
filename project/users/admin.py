import django.contrib.admin
import django.contrib.auth.admin
import django.utils.safestring
from django.utils.translation import gettext as _
import sorl.thumbnail.admin

import users.models

__all__ = []


class ImageInline(
    sorl.thumbnail.admin.AdminImageMixin,
    django.contrib.admin.TabularInline,
):
    fields = [users.models.Image.image.field.name]
    model = users.models.Image


@django.contrib.admin.register(users.models.User)
class UserAdmin(django.contrib.auth.admin.UserAdmin):
    list_display = (users.models.User.username.field.name,)
    avatar_field = (
        users.models.User.avatar.field.name,
        "avatar_preview",
    )
    list_add_fields = [
        users.models.User.birthday.field.name,
        users.models.User.bio.field.name,
        users.models.User.tg_link.field.name,
        users.models.User.rating.field.name,
        avatar_field,
    ]
    readonly_fields = [
        "avatar_preview",
    ]
    fieldsets = django.contrib.auth.admin.UserAdmin.fieldsets + (
        (
            _("profile"),
            {
                "fields": list_add_fields,
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "email", "password1", "password2"),
            },
        ),
    )
    inlines = (ImageInline,)

    def avatar_preview(self, obj):
        if obj:
            return django.utils.safestring.mark_safe(
                f'<img src="{obj.get_image_preview_x50().url}" width="50">',
            )

        return _("no_avatar")

    avatar_preview.short_description = _("avatar_image")
    avatar_preview.allow_tags = True


@django.contrib.admin.register(users.models.Image)
class ImageAdmin(django.contrib.admin.ModelAdmin):
    list_display = (users.models.Image.user.field.name,)
