import django.urls

import streetsport.apps
import streetsport.views

app_name = streetsport.apps.StreetsportConfig.name

urlpatterns = [
    django.urls.path(
        "orders/",
        streetsport.views.GamesListView.as_view(),
        name="orders",
    ),
    django.urls.path(
        "order/create/",
        streetsport.views.GamesCreateView.as_view(),
        name="order-create",
    ),
    django.urls.path(
        "order/<int:pk>/edit/",
        streetsport.views.GamesEditView.as_view(),
        name="order-edit",
    ),
    django.urls.path(
        "order/<int:pk>/delete/",
        streetsport.views.GamesDeleteView.as_view(),
        name="order-delete",
    ),
    django.urls.path(
        "order/<int:pk>/",
        streetsport.views.GamesDetailView.as_view(),
        name="order",
    ),
    django.urls.path(
        "team/<int:pk>/",
        streetsport.views.TeamDetailView.as_view(),
        name="team",
    ),
    django.urls.path(
        "team/create/",
        streetsport.views.TeamCreateView.as_view(),
        name="team-create",
    ),
    django.urls.path(
        "team/<int:pk>/edit/",
        streetsport.views.TeamUpdateView.as_view(),
        name="team-edit",
    ),
    django.urls.path(
        "team/<int:pk>/delete/",
        streetsport.views.TeamDeleteView.as_view(),
        name="team-delete",
    ),
    django.urls.path(
        "user/<int:pk>/add/",
        # TODO: добавить view для добавления юзера в команду текущего юзера(лида)
        streetsport.views.TeamDetailView.as_view(),
        name="team-add",
    ),
    django.urls.path(
        "team/<int:pk>/vs/",
        # TODO: добавить view для создания матча с этой командой(только для лида)
        streetsport.views.TeamDetailView.as_view(),
        name="team-vs",
    ),
]
