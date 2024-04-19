import json

import django.contrib.auth.mixins
import django.views.generic

import streetsport.forms
import streetsport.models
import users.models

__all__ = []


class GamesListView(django.views.generic.ListView):
    model = streetsport.models.Order
    context_object_name = "orders"
    queryset = streetsport.models.Order.objects.homepage()
    template_name = "streetsport/index.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context["qs_users"] = json.dumps(
            list(
                users.models.User.objects.values(
                    "id",
                    "username",
                    "first_name",
                    "last_name",
                )
            ),
            default=str,
        )
        context["qs_teams"] = json.dumps(
            list(
                streetsport.models.Team.objects.values(
                    "id",
                    "title",
                )
            ),
            default=str,
        )
        context["qs_games"] = json.dumps(
            list(
                streetsport.models.Game.objects.values(
                    "id",
                    "title",
                )
            ),
            default=str,
        )
        return context


class GamesCreateView(
    django.contrib.auth.mixins.LoginRequiredMixin,
    django.views.generic.edit.CreateView,
):
    form_class = streetsport.forms.StreetsportOrderModelForm
    template_name = "streetsport/order_create.html"


class GamesDetailView(django.views.generic.detail.DetailView):
    queryset = streetsport.models.Order.objects.all()
    template_name = "streetsport/order.html"
