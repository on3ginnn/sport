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
        "create/",
        streetsport.views.GamesCreateView.as_view(),
        name="order-create",
    ),
    path(
        "<int:pk>/",
        streetsport.views.GamesDetailView.as_view(),
        name="order",
    ),
    path(
        "leaderboard/",
        streetsport.views.GamesListView.as_view(),
        name="leaderboard",
    ),
]
