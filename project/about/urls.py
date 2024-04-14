import django.urls

import about.views

app_name = "about"

urlpatterns = [
    django.urls.path(
        "",
        about.views.DescriptionTemplateView.as_view(),
        name="main",
    ),
]
