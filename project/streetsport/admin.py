from django.contrib import admin

import streetsport.models

__all__ = []


@admin.register(streetsport.models.Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = (streetsport.models.Team.title.field.name,)
    filter_horizontal = (streetsport.models.Team.teammates.field.name,)


@admin.register(streetsport.models.Game)
class GameAdmin(admin.ModelAdmin):
    list_display = (streetsport.models.Game.title.field.name,)
