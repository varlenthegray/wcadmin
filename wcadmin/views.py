from dateutil.relativedelta import relativedelta
from django.views import generic
# from jobsite.models import JobSite
from customer.models import JobSite
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin


class DashboardView(LoginRequiredMixin, generic.ListView):
    model = JobSite
    queryset = JobSite.objects.filter(active=True)[:10]
    template_name = "base.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["service_past_due_total"] = JobSite.objects.filter(next_service_date__year=timezone.now().year)\
            .filter(next_service_date__month=(timezone.now().month - 1)).filter(active=True)
        context["service_past_due"] = context["service_past_due_total"].filter(next_service_date__lt=timezone.now())\
            .filter(active=True)

        context["service_due_total"] = JobSite.objects.filter(next_service_date__year=timezone.now().year)\
            .filter(next_service_date__month=timezone.now().month).filter(active=True)
        context["service_due"] = context["service_due_total"].filter(next_service_date__lt=timezone.now())\
            .filter(active=True)

        context["service_coming_up_total"] = JobSite.objects.filter(next_service_date__year=timezone.now().year)\
            .filter(next_service_date__month=(timezone.now().month + 1)).filter(active=True)
        context["service_coming_up"] = context["service_coming_up_total"].filter(next_service_date__lt=timezone.now())\
            .filter(active=True)

        context["service_refresh_total"] = JobSite.objects.filter(next_service_date__year=(timezone.now().year - 3))\
            .filter(next_service_date__month=timezone.now().month).filter(active=True)
        context["service_refresh"] = context["service_refresh_total"].filter(next_service_date__gt=timezone.now())\
            .filter(active=True)

        context["service_past_due_date"] = timezone.now() - relativedelta(months=1)
        context["service_due_date"] = timezone.now()
        context["service_coming_up_date"] = timezone.now() + relativedelta(months=1)
        context["service_refresh_date"] = timezone.now() - relativedelta(years=3)

        return context
