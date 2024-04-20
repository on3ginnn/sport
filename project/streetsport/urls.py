import django.urls

import streetsport.apps
import streetsport.views

app_name = streetsport.apps.StreetsportConfig.name

urlpatterns = [
    django.urls.path(
        "",
        streetsport.views.GamesListView.as_view(),
        name="orders",
    ),
    django.urls.path(
        "create/",
        streetsport.views.GamesCreateView.as_view(),
        name="order-create",
    ),
    django.urls.path(
        "<int:pk>/",
        streetsport.views.GamesDetailView.as_view(),
        name="order",
    ),
    django.urls.path(
        "leaderboard/",
        streetsport.views.GamesListView.as_view(),
        name="leaderboard",
    ),
]
