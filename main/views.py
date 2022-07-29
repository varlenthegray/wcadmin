import logging

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.postgres.search import SearchVector, SearchQuery
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
            Q(first_name__icontains=search_term) |
            Q(last_name__icontains=search_term) |
            Q(quickbooks_id__icontains=search_term) |
            Q(email__icontains=search_term) |
            Q(phone_number__icontains=search_term) |
            Q(address__icontains=search_term) |
            Q(city__icontains=search_term) |
            Q(state__icontains=search_term) |
            Q(zip__icontains=search_term)
        )
    else:
        job_sites = JobSite.objects.all().prefetch_related('customer')

    data = []

    for job in job_sites:
        name = Truncator(job.display_name).chars(25)

        this_job = {'value': name}

        # if job.first_name: this_job['tokens'].append(job.first_name)
        # if job.last_name: this_job['tokens'].append(job.last_name)
        # if job.email: this_job['tokens'].append(job.email)
        # if job.phone_number: this_job['tokens'].append(job.phone_digits_only())
        #
        # if job.customer.company: this_job['tokens'].append(job.customer.company)
        # if job.customer.first_name: this_job['tokens'].append(job.customer.first_name)
        # if job.customer.last_name: this_job['tokens'].append(job.customer.last_name)
        # if job.customer.email: this_job['tokens'].append(job.customer.email)
        # if job.customer.main_phone: this_job['tokens'].append(job.customer.phone_digits_only())

        data.append(this_job)

    return JsonResponse(data, safe=False)
