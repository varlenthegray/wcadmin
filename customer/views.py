import logging
import simplejson

from django.contrib.postgres.search import SearchVector
from django.shortcuts import render
from django.utils import timezone
from django.views import generic
from django.http import HttpResponseRedirect, HttpResponseBadRequest, HttpResponse, JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin

from rest_framework import viewsets
from datetime import datetime, timedelta

from .models import Customer, JobSite, JobSiteEquipment
# from jobsite.models import JobSite, JobSiteEquipment
from equipment.models import Equipment
from qb.models import Invoice
from .forms import AddCustomerForm, ViewCustomerForm, ViewJobSiteForm, EditJobSiteEquipment, AddJobSiteEquipment, \
    AddJobSiteForm
from .serializers import JobSitesSerializer


logger = logging.getLogger(__name__)


class AllCustomers(LoginRequiredMixin, generic.ListView):
    model = Customer
    queryset = Customer.objects.all()
    template_name = 'customer/all_customers.html'


class CustomersDueThisMonth(LoginRequiredMixin, generic.ListView):
    model = JobSite
    template_name = 'customer/reports/due_this_month.html'


class CustomersDueNextMonth(LoginRequiredMixin, generic.ListView):
    model = JobSite
    template_name = 'customer/reports/due_next_month.html'


class CustomersDueTwoMonthsFuture(LoginRequiredMixin, generic.ListView):
    model = JobSite
    template_name = 'customer/reports/due_two_months_future.html'


class CustomersDueLastMonth(LoginRequiredMixin, generic.ListView):
    model = JobSite
    template_name = 'customer/reports/due_last_month.html'


class CustomersDueLastThreeMonths(LoginRequiredMixin, generic.ListView):
    model = JobSite
    template_name = 'customer/reports/due_last_three_months.html'


class CustomersDueLastYearThisMonth(LoginRequiredMixin, generic.ListView):
    model = JobSite
    template_name = 'customer/reports/due_last_year_this_month.html'


class CustomersCustomReport(LoginRequiredMixin, generic.ListView):
    model = JobSite
    template_name = 'customer/reports/custom_report.html'


class AddCustomer(LoginRequiredMixin, generic.CreateView):
    model = Customer
    template_name = 'customer/add_customer.html'
    form_class = AddCustomerForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            # Placing the ** before it tells the model to treat form.cleaned_data as a dictionary of keyword arguments
            Customer.objects.create(**form.cleaned_data)
            return HttpResponseRedirect('/')
        else:
            return HttpResponseBadRequest('/customer/add')


class ViewCustomer(LoginRequiredMixin, generic.UpdateView):
    model = Customer
    template_name = 'customer/customer.html'
    form_class = ViewCustomerForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['customer_id'] = self.object.pk
        context['cust_obj'] = Customer.objects.get(pk=context['customer_id'])
        context['customer'] = ViewCustomerForm(instance=context['cust_obj'], prefix='customer')

        context['job_obj'] = JobSite.objects.filter(customer=context['customer_id']).first()
        context['jobsite'] = ViewJobSiteForm(instance=context['job_obj'], prefix='job')
        context['all_job_sites'] = JobSite.objects.filter(customer=context['customer_id'])

        context['invoice'] = Invoice.objects.filter(job_site=context['job_obj']).prefetch_related('invoiceline_set')

        context['current_date'] = datetime.now()

        if context['job_obj']:
            context['job_site_id'] = context['job_obj'].pk
            context['existing_equipment'] = JobSiteEquipment.objects.filter(job_site=context['job_obj'].pk)
        else:
            context['job_site_id'] = 0

        context['add_equipment_form'] = AddJobSiteEquipment(prefix='equipment')
        return context


class ViewSpecificJobSite(LoginRequiredMixin, generic.UpdateView):
    model = JobSite
    template_name = 'customer/customer.html'
    form_class = ViewJobSiteForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['customer'] = ViewCustomerForm(instance=self.object.customer, prefix='customer')
        context['customer_id'] = self.object.customer.pk
        context['cust_obj'] = Customer.objects.get(pk=context['customer_id'])

        context['job_site_id'] = self.object.pk
        context['jobsite'] = ViewJobSiteForm(instance=JobSite.objects.get(pk=context['job_site_id']), prefix='job')
        context['job_obj'] = JobSite.objects.get(pk=context['job_site_id'])
        context['all_job_sites'] = JobSite.objects.filter(customer=self.object.customer)

        context['existing_equipment'] = JobSiteEquipment.objects.filter(job_site=context['job_site_id'])
        context['all_equipment'] = Equipment.objects.all().order_by('name')
        context['add_equipment_form'] = AddJobSiteEquipment(prefix='equipment')

        context['invoice'] = Invoice.objects.filter(job_site=context['job_site_id']).prefetch_related('invoiceline_set')

        context['current_date'] = datetime.now()

        return context


class ViewDeleteEquipmentFromJobSite(LoginRequiredMixin, generic.DeleteView):
    model = JobSiteEquipment
    template_name = 'customer/job_sites/job_site.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return HttpResponse('success')


class ViewEditEquipmentLine(LoginRequiredMixin, generic.UpdateView):
    model = JobSiteEquipment
    template_name = 'customer/job_sites/edit_equipment_line.html'
    form_class = EditJobSiteEquipment

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['equipment_line_id'] = self.object.pk
        return context


class AddJobSiteToCustomer(LoginRequiredMixin, generic.CreateView):
    model = JobSite
    template_name = 'customer/job_sites/form.html'
    form_class = AddJobSiteForm
    form2 = AddJobSiteForm(prefix='jstc')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form2'] = self.form2
        return context


class SaveJobSiteToCustomer(LoginRequiredMixin, generic.CreateView):
    model = JobSite
    template_name = 'customer/job_sites/form.html'
    form_class = AddJobSiteForm

    def post(self, request, *args, **kwargs):
        customer = Customer.objects.get(pk=request.POST['customer_id'])
        add_job_site_customer = AddJobSiteForm(request.POST, prefix='job')

        if add_job_site_customer.is_valid():
            jobsite_save = add_job_site_customer.save(commit=False)
            jobsite_save.customer = customer
            jobsite_save.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            return HttpResponseBadRequest(add_job_site_customer.errors)


class UpdateJobSite(LoginRequiredMixin, generic.UpdateView):
    model = JobSite
    template_name = 'customer/job_sites/form.html'
    form_class = ViewJobSiteForm

    def post(self, request, *args, **kwargs):
        job_site = JobSite.objects.get(pk=self.kwargs['pk'])
        job_site_form = AddJobSiteForm(request.POST, instance=job_site, prefix='job')

        if job_site_form.is_valid():
            job_site_form.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            logger.warning('Unable to update job site ' + self.kwargs['pk'])
            return HttpResponseBadRequest(job_site_form.errors)


class SaveCustomer(LoginRequiredMixin, generic.CreateView):
    model = Customer
    template_name = 'customer/customer.html'
    form_class = ViewCustomerForm

    def post(self, request, *args, **kwargs):
        customer = Customer.objects.get(pk=request.POST['customer_id'])
        update_customer = ViewCustomerForm(request.POST, instance=customer, prefix='customer')

        if update_customer.is_valid():
            update_customer.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            return HttpResponseBadRequest(update_customer.errors)


class SaveEquipmentChanges(LoginRequiredMixin, generic.UpdateView):
    model = JobSiteEquipment
    template_name = 'customer/job_sites/edit_equipment_line.html'
    form_class = EditJobSiteEquipment

    def post(self, request, *args, **kwargs):
        equipment = JobSiteEquipment.objects.get(pk=self.kwargs['pk'])
        save_equipment = EditJobSiteEquipment(request.POST, instance=equipment)

        if save_equipment.is_valid():
            save_equipment.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            return HttpResponseBadRequest(save_equipment.errors)


class AddEquipmentToJobSite(LoginRequiredMixin, generic.CreateView):
    model = JobSiteEquipment
    template_name = 'customer/job_sites/add_equipment_jobsite.html'
    form_class = AddJobSiteEquipment

    def post(self, request, *args, **kwargs):
        add_equipment_jobsite = AddJobSiteEquipment(request.POST, prefix='equipment')

        if add_equipment_jobsite.is_valid():
            data = add_equipment_jobsite.save(commit=False)

            data.added_by = request.user
            data.job_site = JobSite.objects.get(pk=request.POST['job_id'])

            data.save()

            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            return HttpResponseBadRequest(add_equipment_jobsite.errors)


class AllJobSites(LoginRequiredMixin, generic.ListView):
    model = JobSite
    queryset = JobSite.objects.all().prefetch_related('customer')
    template_name = 'customer/job_sites/all_jobsites.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        context['job_sites'] = self.queryset

        return context


class ViewJobSite(LoginRequiredMixin, generic.UpdateView):
    model = JobSite
    form_class = ViewJobSiteForm
    template_name = 'customer/job_sites/view_jobsite.html'


class AddJobSite(LoginRequiredMixin, generic.CreateView):
    model = JobSite
    form_class = ViewJobSiteForm
    template_name = 'customer/job_sites/add_jobsite.html'


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
            base_query = JobSite.objects.filter(active=True).filter(disable_service=False)

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

        return base_query


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


def print_address_labels(request, *args, **kwargs):
    # fancy footwork to get POST data and represent it as an array, then get objects from the array
    raw_job_site_ids = simplejson.loads(request.POST['data'])['body']
    job_site_ids = []

    # this has to be done, it's a 3D array initially with 1 array, [0] didn't work
    for js_id in raw_job_site_ids:
        job_site_ids.append(js_id[0])

    job_sites = JobSite.objects.filter(pk__in=job_site_ids)
    context = {'jobsite': job_sites}

    return render(request, 'customer/address_labels.html', context)


class PrintAddressLabels(LoginRequiredMixin, generic.ListView):
    model = JobSite
    template_name = 'customer/address_labels.html'

    def post(self, request, *args, **kwargs):
        return HttpResponse(status=200)
