__all__ = []

import django.shortcuts
import django.views
import django.views.generic

import search.forms


class SearchListView(django.views.generic.FormView):
    template_name = "search/search.html"
    form_class = search.forms.SearchForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search_value = context["form"].data["search-header"]
        print(search_value)
        # TODO: search_value - запрос. Найти похожие и передать в контекст 2 переменные(users, teams).
        # TODO: Каждая перменная хранит инфу для таблицы search:search.
        # TODO:
        context["form"].data["search-header"] = search_value
        return context
