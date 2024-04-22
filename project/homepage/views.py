import django.views.generic

import streetsport.models

__all__ = []


class HomeView(django.views.generic.ListView):
    model = streetsport.models.Order
    context_object_name = "orders"
    # TODO: баг: ордер с 19:00, 01.05.2024 раньше чем 13:30, 28.04.2024
    queryset = streetsport.models.Order.objects.homepage()
    template_name = "homepage/index.html"
