import logging

from django.http import JsonResponse, HttpResponse
from django.utils import timezone
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.postgres.search import SearchVector

from datetime import datetime, timedelta
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
        order = self.request.GET.get('order[0][column]')
        order_direction = self.request.GET.get('order[0][dir]')
        report_info = self.request.GET.get('report')

        all_items = self.request.GET.get('all_items')

        # Custom report fields
        from_date = self.request.GET.get('fromDate')
        to_date = self.request.GET.get('toDate')

        if order == 1:
            order_by_column = 'name'
        elif order == 5:
            order_by_column = 'next_service_date'
        elif order == 6:
            order_by_column = 'service_scheduled'
        else:
            order_by_column = 'id'

        if order_direction == 'desc':
            order_direction = '-'
        else:
            order_direction = ''

        if all_items:
            base_query = JobSite.objects.all()
        else:
            base_query = JobSite.objects.filter(active=True)

        if search:
            base_query = JobSite.objects.annotate(
                search=SearchVector('quickbooks_id', 'name', 'address', 'address_2', 'city', 'state', 'zip',
                                    'phone_number', 'email', 'customer__company', 'invoice__invoice_num')
            ).filter(search__icontains=search)

        if report_info == 'last_month':
            base_query = base_query.filter(next_service_date__month=(timezone.now().month - 1)) \
                .filter(next_service_date__year=timezone.now().year).filter(active=True)
        elif report_info == 'this_month':
            base_query = base_query.filter(next_service_date__month=timezone.now().month) \
                .filter(next_service_date__year=timezone.now().year).filter(active=True)
        elif report_info == 'next_month':
            base_query = base_query.filter(next_service_date__month=(timezone.now().month + 1)) \
                .filter(next_service_date__year=timezone.now().year).filter(active=True)
        elif report_info == 'next_two_months':
            base_query = base_query.filter(next_service_date__month=(timezone.now().month + 2)) \
                .filter(next_service_date__year=timezone.now().year).filter(active=True)
        elif report_info == 'past_three_months':
            base_query = base_query.filter(next_service_date__gt=(datetime.now() - timedelta(weeks=12))) \
                .filter(next_service_date__lt=timezone.now()).filter(next_service_date__year=timezone.now().year) \
                .filter(active=True)
        elif report_info == 'last_year_this_month':
            base_query = base_query.filter(next_service_date__month=timezone.now().month) \
                .filter(next_service_date__year=(timezone.now().year - 1)).filter(active=True)
        elif report_info == 'custom_report':
            if from_date:
                from_date = datetime.strptime(from_date, '%m-%d-%Y').strftime('%Y-%m-%d')
                base_query = base_query.filter(next_service_date__gte=from_date)

            if to_date:
                to_date = datetime.strptime(to_date, '%m-%d-%Y').strftime('%Y-%m-%d')
                base_query = base_query.filter(next_service_date__lte=to_date)

        if order:
            base_query = base_query.order_by(order_direction + order_by_column)

        self.queryset = base_query

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
