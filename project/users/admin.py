from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from sorl.thumbnail.admin import AdminImageMixin

import users.models

__all__ = []


class ImageInline(AdminImageMixin, admin.TabularInline):
    fields = [users.models.Image.image.field.name]
    model = users.models.Image


@admin.register(users.models.User)
class UserAdmin(UserAdmin):
    list_display = (users.models.User.username.field.name,)
    inlines = (ImageInline,)


@admin.register(users.models.Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = (users.models.Image.image.field.name,)
