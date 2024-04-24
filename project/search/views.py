__all__ = []

import django.shortcuts
import django.views
import django.views.generic

import search.forms
import streetsport.models
import users.models


class SearchListView(django.views.generic.FormView):
    template_name = "search/search.html"
    form_class = search.forms.SearchForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search_value = context["form"].data["search-header"]
        context["users"] = users.models.User.objects.search_by_username(
            search_value,
        )
        context["teams"] = streetsport.models.Team.objects.search_by_title(
            search_value,
        )
        return context
