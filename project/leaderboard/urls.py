__all__ = []

import django.urls

import leaderboard.apps
import leaderboard.views

app_name = leaderboard.apps.LeaderboardConfig.name

urlpatterns = [
    django.urls.path(
        "users/",
        leaderboard.views.UsersTopListView.as_view(),
        name="users",
    ),
    django.urls.path(
        "teams/",
        leaderboard.views.TeamsTopListView.as_view(),
        name="teams",
    ),
]
