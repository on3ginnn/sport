import json

import django.contrib.auth.mixins
import django.db.models
import django.http
import django.shortcuts
import django.urls
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


class TeamCreateView(
    django.contrib.auth.mixins.LoginRequiredMixin,
    django.views.generic.CreateView,
):
    form_class = streetsport.forms.TeamEditForm
    success_url = django.urls.reverse_lazy("homepage:main")
    template_name = "streetsport/team_edit.html"

    def form_valid(self, form):
        form.save()
        self.request.user.lead_team = form.instance
        self.request.user.team = form.instance
        self.request.user.save()
        return super().form_valid(form)


class TeamDetailView(django.views.generic.DetailView):
    template_name = "streetsport/team.html"
    queryset = streetsport.models.Team.objects.detail()
    context_object_name = "team"

    def get_context_data(self, **kwargs):
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
        return super().get_context_data(**kwargs)


class TeamUpdateView(django.views.generic.UpdateView):
    success_message = _("team_edit_success")
    form_class = streetsport.forms.TeamEditForm
    template_name = "streetsport/team_edit.html"

    def get_object(self, *args, **kwargs):
        self.success_url = django.urls.reverse_lazy(
            "streetsport:team", kwargs={"pk": self.request.user.team.id}
        )
        return self.request.user.team


class GamesListView(django.views.generic.ListView):
    model = streetsport.models.Order
    context_object_name = "orders"
    queryset = streetsport.models.Order.objects.homepage()
    template_name = "streetsport/index.html"

    def get_queryset(self):
        return reversed(super().get_queryset())

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


class GamesRedirectView(django.views.generic.RedirectView):
    url = django.urls.reverse_lazy("homepage:main")

    def get(self, request, *args, **kwargs):
        order = django.shortcuts.get_object_or_404(
            streetsport.models.Order,
            **kwargs,
        )
        order.delete()
        return super().get(request, *args, **kwargs)


class GamesEditView(
    django.contrib.auth.mixins.LoginRequiredMixin,
    django.views.generic.edit.UpdateView,
):
    form_class = streetsport.forms.StreetsportOrderModelForm
    template_name = "streetsport/order_create.html"
    queryset = streetsport.models.Order.objects.all()

    def get_success_url(self):
        return django.urls.reverse_lazy(
            "streetsport:order", kwargs={"pk": self.kwargs["pk"]}
        )


class GamesCreateView(
    django.contrib.auth.mixins.LoginRequiredMixin,
    django.views.generic.edit.CreateView,
):
    form_class = streetsport.forms.StreetsportOrderModelForm
    success_url = django.urls.reverse_lazy("homepage:main")

    def get(self, request, *args, **kwargs):
        if not self.request.user.lead_team:
            raise django.http.Http404

        return super().get(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["initial"][
            streetsport.models.Order.team_one.field.name
        ] = self.request.user.lead_team
        return kwargs

    template_name = "streetsport/order_create.html"


class GamesDetailView(django.views.generic.detail.DetailView):
    queryset = streetsport.models.Order.objects.all()
    template_name = "streetsport/order.html"


class TeammateAddRedirectView(
    django.contrib.auth.mixins.LoginRequiredMixin,
    django.views.generic.RedirectView,
):
    def get(self, request, *args, **kwargs):
        user = django.shortcuts.get_object_or_404(users.models.User, **kwargs)
        if request.user.lead_team and not user.team:
            user.team = request.user.lead_team
        else:
            raise django.http.Http404

        return super().get(request, *args, **kwargs)


class OrderCreateView(
    django.contrib.auth.mixins.LoginRequiredMixin,
    django.views.generic.CreateView,
):
    form_class = streetsport.forms.StreetsportOrderModelForm
    template_name = "streetsport/order_create.html"
    success_url = django.urls.reverse_lazy("homepage:main")

    def get(self, request, *args, **kwargs):
        if not self.request.user.lead_team:
            raise django.http.Http404

        return super().get(request, *args, **kwargs)

    def get_form_kwargs(self):
        team_two = django.shortcuts.get_object_or_404(
            streetsport.models.Team,
            **self.kwargs,
        )
        kwargs = super().get_form_kwargs()
        kwargs["initial"][
            streetsport.models.Order.team_one.field.name
        ] = self.request.user.lead_team
        kwargs["initial"][
            streetsport.models.Order.team_two.field.name
        ] = team_two
        return kwargs

    def get_form(self):
        form = super().get_form()
        form.fields[streetsport.models.Order.team_two.field.name].disabled = (
            True
        )
        return form
