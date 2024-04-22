import json

import django.contrib.auth.mixins
import django.db.models
import django.http
from django.utils.translation import gettext_lazy as _
import django.views.generic

import streetsport.forms
import streetsport.models
import users.models

__all__ = []


class TeamDeleteView(
    django.contrib.auth.mixins.LoginRequiredMixin,
    django.views.generic.DeleteView,
):
    template_name = "streetsport/team.html"
    queryset = streetsport.models.Team.objects.delete_view()

    def get(self, request, *args, **kwargs):
        if self.request.user != self.get_object().lead:
            raise django.http.Http404

        return super().get(request, *args, **kwargs)

    queryset = streetsport.models.Team.objects.all()


class TeamCreateView(django.views.generic.CreateView):
    form_class = streetsport.forms.TeamEditForm
    template_name = "streetsport/team_edit.html"
    


class TeamDetailView(django.views.generic.DetailView):
    template_name = "streetsport/team.html"
    queryset = streetsport.models.Team.objects.detail()
    context_object_name = "team"

    def get_context_data(self, **kwargs):
        # TODO: в teammates загрузить всех участников команды (поля: id, username, avatar, single_top, lead_status(lead or not))

        kwargs.update(
            self.queryset.aggregate(
                team_top=django.db.models.Count(
                    "id",
                    filter=django.db.models.Q(
                        rating__gte=kwargs.get("object").rating
                    ),
                )
            )
        )
        # TODO: error: The QuerySet value for an exact lookup must be limited to one result using slicing.
        self.extra_context = {
            "teammates": users.models.User.objects.filter(
                team__id=self.queryset
            ).order_by("-rating")
        }
        return super().get_context_data(**kwargs)


class TeamUpdateView(django.views.generic.UpdateView):
    success_message = _("team_edit_success")
    form_class = streetsport.forms.TeamEditForm
    template_name = "streetsport/team_edit.html"

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


class GamesDeleteView(django.views.generic.DeleteView):
    # TODO: сделать удаление ордера streetport:order-delete
    pass


class GamesEditView(
    django.contrib.auth.mixins.LoginRequiredMixin,
    django.views.generic.edit.UpdateView,
):
    form_class = streetsport.forms.StreetsportOrderModelForm
    template_name = "streetsport/order_create.html"
    queryset = streetsport.models.Order.objects.all()

    def get_success_url(self):
        return django.urls.reverse_lazy("streetsport:order", kwargs={"pk":self.kwargs['pk']})


class GamesCreateView(
    django.contrib.auth.mixins.LoginRequiredMixin,
    django.views.generic.edit.CreateView,
):
    form_class = streetsport.forms.StreetsportOrderModelForm
    template_name = "streetsport/order_create.html"


class GamesDetailView(django.views.generic.detail.DetailView):
    queryset = streetsport.models.Order.objects.all()
    template_name = "streetsport/order.html"
