from django.contrib import admin

import users.models

__all__ = []

admin.site.register(users.models.User)
