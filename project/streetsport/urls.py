from django.urls import path

from feedback import views
import streetsport.apps

app_name = streetsport.apps.StreetsportConfig.name

urlpatterns = [
    path(
        "",
        views.FeedbackCreateView.as_view(),
        name="orders",
    ),
    path(
        "",
        views.FeedbackCreateView.as_view(),
        name="leaderboard",
    ),
]
