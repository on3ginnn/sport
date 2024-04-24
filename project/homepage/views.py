import django.views.generic

import streetsport.models

__all__ = []


class HomeView(django.views.generic.ListView):
    model = streetsport.models.Order
    context_object_name = "orders"
    queryset = reversed(streetsport.models.Order.objects.homepage())
    template_name = "homepage/index.html"
