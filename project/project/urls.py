from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path(
        "",
        include(
            "homepage.urls",
        ),
        name="homepage",
    ),
    path(
        "about/",
        include(
            "about.urls",
        ),
        name="about",
    ),
    path(
        "feedback/",
        include(("feedback.urls")),
        name="feedback",
    ),
    path(
        "admin/",
        admin.site.urls,
    ),
]


if settings.DEBUG:
    urlpatterns += (path("__debug__/", include("debug_toolbar.urls")),)
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )
