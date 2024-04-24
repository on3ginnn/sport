import django.views.generic

import streetsport.models

__all__ = []


class HomeView(django.views.generic.ListView):
    model = streetsport.models.Order
    context_object_name = "orders"
    queryset = streetsport.models.Order.objects.homepage()

    def get_queryset(self):

        return reversed(super().get_queryset())

    template_name = "homepage/index.html"
