import django.urls

import leaderboard.apps
import leaderboard.views

app_name = leaderboard.apps.LeaderboardConfig.name

urlpatterns = [
    django.urls.path(
        "",
        leaderboard.views.LeaderboardListView.as_view(),
        name="main",
    )
]
