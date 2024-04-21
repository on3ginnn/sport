import json

import django.contrib.auth.mixins
from django.utils.translation import gettext_lazy as _
import django.views.generic

import streetsport.forms
import streetsport.models
import users.models

__all__ = []


class TeamDeleteView(django.views.generic.DeleteView):
    template_name = "streetsport/team.html"
    # TODO: оптимизировать запрос и сделать чтобы работало(только для лида)
    queryset = streetsport.models.Team.objects.all()


class TeamDetailView(django.views.generic.DetailView):
    template_name = "streetsport/team.html"
    queryset = streetsport.models.Team.objects.all()
    context_object_name = "team"
    # TODO: оптимизировать запрос
    # TODO: получить место команды(team_top) в топе( order_by("-raging", "title") )
    extra_context = {"teams": streetsport.models.Team.objects.all()}


class TeamUpdateView(django.views.generic.UpdateView):
    success_message = _("team_edit_success")
    form_class = streetsport.forms.TeamEditForm
    template_name = "streetsport/team_edit.html"

    # TODO: нужно получить команду текущего юзера (переделать связь команды и игрока с ManyToMany на OneToMany (игрок только в одной команде, в команде много игроков))
    def get_object(self, *args, **kwargs):
        self.success_url = django.urls.reverse_lazy(
            "streetsport:team", kwargs={"pk": self.request.user.teams.id}
        )
        return self.request.user.teams


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
                    "normalize_title",
                )
            ),
            default=str,
        )
        context["qs_games"] = json.dumps(
            list(
                streetsport.models.Game.objects.values(
                    "id",
                    "title",
                    "normalize_title",
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
