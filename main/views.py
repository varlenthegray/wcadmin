import logging

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.text import Truncator
from django.db.models import Q
from django.http import JsonResponse
from django.views import generic

from .models import VersionLog
from customer.models import JobSite

logger = logging.getLogger(__name__)


class GetChangeLog(LoginRequiredMixin, generic.ListView):
    model = VersionLog
    queryset = VersionLog.objects.all()
    template_name = 'main/change_log.html'


@login_required
def search_system(request, search_term=False):
    if search_term:
        job_sites = JobSite.objects.filter(
            Q(first_name__icontains=search_term) | Q(last_name__icontains=search_term) |
            Q(quickbooks_id__icontains=search_term) | Q(email__icontains=search_term) |
            Q(phone_number__icontains=search_term) | Q(address__icontains=search_term) |
            Q(city__icontains=search_term) | Q(state__icontains=search_term) | Q(zip__icontains=search_term) |
            Q(customer__company__icontains=search_term)
        )
    else:
        job_sites = JobSite.objects.all().prefetch_related('customer')

    data = []

    for job in job_sites:
        name = Truncator(job.display_name).chars(25)

        this_job = {'value': name, 'id': job.pk}

        data.append(this_job)

    return JsonResponse(data, safe=False)
