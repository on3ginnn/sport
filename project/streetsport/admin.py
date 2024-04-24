import django.contrib.admin
import django.forms

import streetsport.models
import users.models

__all__ = []


class TeammatesInline(django.contrib.admin.TabularInline):
    fields = [users.models.User.username.field.name]
    readonly_fields = [users.models.User.username.field.name]
    fk_name = "team"
    model = users.models.User


class LeadInline(django.contrib.admin.TabularInline):
    fields = [users.models.User.username.field.name]
    readonly_fields = [users.models.User.username.field.name]
    fk_name = "lead_team"
    model = users.models.User


@django.contrib.admin.register(streetsport.models.Team)
class TeamAdmin(django.contrib.admin.ModelAdmin):
    list_display = (streetsport.models.Team.title.field.name,)
    inlines = (TeammatesInline, LeadInline)


@django.contrib.admin.register(streetsport.models.Game)
class GameAdmin(django.contrib.admin.ModelAdmin):
    list_display = (streetsport.models.Game.title.field.name,)


@django.contrib.admin.register(streetsport.models.Order)
class OrderAdmin(django.contrib.admin.ModelAdmin):
    list_display = (streetsport.models.Order.start.field.name,)
