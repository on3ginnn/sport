import django.conf
import django.conf.urls.static
import django.contrib.admin
import django.contrib.auth.urls
import django.urls

import leaderboard.apps
import leaderboard.urls
import search.apps
import search.urls
import streetsport.apps

urlpatterns = [
    django.urls.path(
        "",
        django.urls.include(
            "homepage.urls",
        ),
        name="homepage",
    ),
    django.urls.path(
        "about/",
        django.urls.include(
            "about.urls",
        ),
        name="about",
    ),
    django.urls.path(
        "feedback/",
        django.urls.include(("feedback.urls")),
        name="feedback",
    ),
    django.urls.path(
        "games/",
        django.urls.include(("streetsport.urls")),
        name=streetsport.apps.StreetsportConfig.name,
    ),
    django.urls.path(
        "auth/",
        django.urls.include(("users.urls")),
        name="users",
    ),
    django.urls.path(
        "admin/",
        django.contrib.admin.site.urls,
    ),
    django.urls.path(
        "auth/",
        django.urls.include(django.contrib.auth.urls),
    ),
    django.urls.path(
        "search/",
        django.urls.include(search.urls),
        name=search.apps.SearchConfig.name,
    ),
    django.urls.path(
        "leaderboard/",
        django.urls.include(leaderboard.urls),
        name=leaderboard.apps.LeaderboardConfig.name,
    ),
]


if django.conf.settings.DEBUG:
    urlpatterns += (
        django.urls.path(
            "__debug__/",
            django.urls.include("debug_toolbar.urls"),
        ),
    )
    urlpatterns += django.conf.urls.static.static(
        django.conf.settings.MEDIA_URL,
        document_root=django.conf.settings.MEDIA_ROOT,
    )
