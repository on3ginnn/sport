from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.safestring import mark_safe
from django.utils.translation import gettext as _
from sorl.thumbnail.admin import AdminImageMixin

import users.models

__all__ = []


class ImageInline(AdminImageMixin, admin.TabularInline):
    fields = [users.models.Image.image.field.name]
    model = users.models.Image


@admin.register(users.models.User)
class UserAdmin(UserAdmin):
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
    fieldsets = UserAdmin.fieldsets + (
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
            return mark_safe(
                f'<img src="{obj.get_image_preview_x50().url}" width="50">',
            )

        return _("no_avatar")

    avatar_preview.short_description = _("avatar_image")
    avatar_preview.allow_tags = True


@admin.register(users.models.Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = (users.models.Image.user.field.name,)
