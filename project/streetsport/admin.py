import django.contrib.admin

import streetsport.models

__all__ = []


@django.contrib.admin.register(streetsport.models.Team)
class TeamAdmin(django.contrib.admin.ModelAdmin):
    list_display = (streetsport.models.Team.title.field.name,)
    filter_horizontal = (streetsport.models.Team.teammates.field.name,)


@django.contrib.admin.register(streetsport.models.Game)
class GameAdmin(django.contrib.admin.ModelAdmin):
    list_display = (streetsport.models.Game.title.field.name,)


@django.contrib.admin.register(streetsport.models.Order)
class OrderAdmin(django.contrib.admin.ModelAdmin):
    list_display = (streetsport.models.Order.start.field.name,)
