from django.urls import path

import streetsport.apps
import streetsport.views

app_name = streetsport.apps.StreetsportConfig.name

urlpatterns = [
    path(
        "",
        streetsport.views.GamesListView.as_view(),
        name="orders",
    ),
    path(
        "leaderboard/",
        streetsport.views.GamesListView.as_view(),
        name="leaderboard",
    ),
]
