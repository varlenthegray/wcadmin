import json

from django.core import serializers
from django.http import JsonResponse
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import JobSite
from .forms import ViewJobSiteForm


class AllJobSites(LoginRequiredMixin, generic.ListView):
    model = JobSite
    queryset = JobSite.objects.all().prefetch_related('customer')
    template_name = 'jobsite/all_jobsites.html'


class ViewJobSite(LoginRequiredMixin, generic.UpdateView):
    model = JobSite
    form_class = ViewJobSiteForm
    template_name = 'jobsite/view_jobsite.html'


class AddJobSite(LoginRequiredMixin, generic.CreateView):
    model = JobSite
    form_class = ViewJobSiteForm
    template_name = 'jobsite/add_jobsite.html'


# def all_job_sites_json(request):
#     job_site_obj = JobSite.objects.values_list(named=True)
#
#     # job_sites = serializers.serialize("json", job_site_obj)
#     return JsonResponse(list(job_site_obj), safe=False)


def all_job_sites_json(request):
    job_site_obj = JobSite.objects.all().values('quickbooks_id', 'name', 'address', 'address_2', 'city', 'state',
                                                'zip', 'phone_number', 'email', 'next_service_date',
                                                'service_scheduled')
    job_site = json.dumps({"data": list(job_site_obj)}, default=str)

    return JsonResponse(job_site, safe=False)
