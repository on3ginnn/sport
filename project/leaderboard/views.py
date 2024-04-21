__all__ = []

import django.shortcuts
import django.views
import django.views.generic

import streetsport.models
import users.models


class LeaderboardListView(django.views.generic.ListView):
    template_name = "leaderboard/leaderboard.html"
    queryset = users.models.User.objects.all().order_by(
        "-rating", "-teams__rating"
    )
    context_object_name = "users"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["teams"] = streetsport.models.Team.objects.all().order_by(
            "-rating", "title"
        )
        return context


class UsersTopListView(django.views.generic.ListView):
    template_name = "leaderboard/users_top.html"
    queryset = users.models.User.objects.all().order_by(
        "-rating", "-teams__rating"
    )
    context_object_name = "users"


class TeamsTopListView(django.views.generic.ListView):
    template_name = "leaderboard/teams_top.html"
    queryset = streetsport.models.Team.objects.all().order_by(
        "-rating", "title"
    )
    context_object_name = "teams"
