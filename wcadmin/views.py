from django.views import generic
from customer.models import Customer
from django.utils import timezone


class DashboardView(generic.ListView):
    model = Customer
    queryset = Customer.objects.filter(next_service__month=timezone.now().month)\
        .filter(next_service__year=timezone.now().year).filter(is_active=True)
    template_name = "base.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["service_past_due_total"] = Customer.objects.filter(next_service__year=timezone.now().year)\
            .filter(next_service__month=(timezone.now().month - 1))
        context["service_past_due"] = context["service_past_due_total"].filter(next_service__lt=timezone.now())

        context["service_due_total"] = Customer.objects.filter(next_service__year=timezone.now().year)\
            .filter(next_service__month=timezone.now().month)
        context["service_due"] = context["service_due_total"].filter(next_service__lt=timezone.now())

        context["service_coming_up_total"] = Customer.objects.filter(next_service__year=timezone.now().year)\
            .filter(next_service__month=(timezone.now().month + 1))
        context["service_coming_up"] = context["service_coming_up_total"].filter(next_service__lt=timezone.now())

        context["service_refresh_total"] = Customer.objects.filter(next_service__year=(timezone.now().year - 1))\
            .filter(next_service__month=timezone.now().month)
        context["service_refresh"] = context["service_refresh_total"].filter(next_service__gt=timezone.now())

        return context
