import django.urls

import search.apps
import search.views

app_name = search.apps.SearchConfig.name

urlpatterns = [
    django.urls.path(
        "",
        search.views.SearchListView.as_view(),
        name="search",
    )
]
