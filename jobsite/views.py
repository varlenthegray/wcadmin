import logging

from django.http import JsonResponse, HttpResponse
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

from rest_framework import viewsets
from .serializers import JobSitesSerializer

from .models import JobSite
from .forms import ViewJobSiteForm

logger = logging.getLogger(__name__)


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


def all_job_sites_json(request):
    job_site_values = JobSite.objects.filter(active=True).prefetch_related('customer') \
        .values('id', 'quickbooks_id', 'name', 'address', 'address_2', 'city', 'state', 'zip', 'phone_number', 'email',
                'next_service_date', 'service_scheduled', 'customer__company')

    return JsonResponse({"data": list(job_site_values)}, safe=False)


class JobSitesREST(viewsets.ModelViewSet):
    queryset = JobSite.objects.filter(active=True).order_by('name')
    serializer_class = JobSitesSerializer

    def get_queryset(self):
        search = self.request.GET.get('search[value]')

        if search:
            logger.warning("WAHOO!!! WE GOT IT BOYS! Search Value: " + search)
        else:
            logger.warning("We didn't get it...")

        return self.queryset


def set_job_site_scheduled(request, *args, **kwargs):
    job_id = kwargs.get('pk')

    if job_id:
        update_job = JobSite.objects.get(pk=job_id)

        update_job.service_scheduled = True
        update_job.save()

        return HttpResponse(status=200, content='Set Job Site as scheduled.')
    else:
        logger.critical('Got request to update scheduled but no ID was provided.')
        return HttpResponse(status=400, content='No PK provided')
