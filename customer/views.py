from django.views import generic
from .models import Customer
from jobsite.models import JobSite, JobSiteEquipment
from equipment.models import Equipment
from qb.models import Invoice, InvoiceLine
from django.http import HttpResponseRedirect, HttpResponseBadRequest, HttpResponse
from .forms import AddCustomerForm, ViewCustomerForm, ViewJobSiteForm, EditJobSiteEquipment, AddJobSiteEquipment, \
    AddJobSiteForm
from django.utils import timezone
from datetime import datetime, timedelta
from django.contrib.auth.mixins import LoginRequiredMixin


class AllCustomers(LoginRequiredMixin, generic.ListView):
    model = Customer
    queryset = Customer.objects.all()
    template_name = 'customer/all_customers.html'


class CustomersDueThisMonth(LoginRequiredMixin, generic.ListView):
    model = JobSite
    queryset = JobSite.objects.filter(next_service_date__month=timezone.now().month) \
        .filter(next_service_date__year=timezone.now().year).filter(active=True)
    template_name = 'customer/reports/due_this_month.html'


class CustomersDueNextMonth(LoginRequiredMixin, generic.ListView):
    model = JobSite
    queryset = JobSite.objects.filter(next_service_date__month=(timezone.now().month + 1)) \
        .filter(next_service_date__year=timezone.now().year).filter(active=True)
    template_name = 'customer/reports/due_next_month.html'


class CustomersDueTwoMonthsFuture(LoginRequiredMixin, generic.ListView):
    model = JobSite
    queryset = JobSite.objects.filter(next_service_date__month=(timezone.now().month + 2)) \
        .filter(next_service_date__year=timezone.now().year).filter(active=True)
    template_name = 'customer/reports/due_two_months_future.html'


class CustomersDueLastMonth(LoginRequiredMixin, generic.ListView):
    model = JobSite
    queryset = JobSite.objects.filter(next_service_date__month=(timezone.now().month - 1)) \
        .filter(next_service_date__year=timezone.now().year).filter(active=True)
    template_name = 'customer/reports/due_last_month.html'


class CustomersDueLastThreeMonths(LoginRequiredMixin, generic.ListView):
    model = JobSite
    queryset = JobSite.objects.filter(next_service_date__gt=(datetime.now() - timedelta(weeks=12))) \
        .filter(next_service_date__lt=timezone.now()).filter(next_service_date__year=timezone.now().year).filter(active=True)
    template_name = 'customer/reports/due_last_three_months.html'


class CustomersDueLastYearThisMonth(LoginRequiredMixin, generic.ListView):
    model = JobSite
    queryset = JobSite.objects.filter(next_service_date__month=timezone.now().month) \
        .filter(next_service_date__year=(timezone.now().year - 1)).filter(active=True)
    template_name = 'customer/reports/due_last_year_this_month.html'


class CustomersCustomReport(LoginRequiredMixin, generic.ListView):
    model = JobSite
    template_name = 'customer/reports/custom_report.html'

    def get_queryset(self):
        from_date = self.request.GET.get('fromDate')
        to_date = self.request.GET.get('toDate')
        self.queryset = JobSite.objects.filter(active=True)

        if from_date:
            from_date = datetime.strptime(from_date, '%m-%d-%Y').strftime('%Y-%m-%d')
            self.queryset = self.queryset.filter(next_service_date__gte=from_date)

        if to_date:
            to_date = datetime.strptime(to_date, '%m-%d-%Y').strftime('%Y-%m-%d')
            self.queryset = self.queryset.filter(next_service_date__lte=to_date)

        return self.queryset


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

        context['invoice'] = Invoice.objects.filter(job_site=context['job_obj'])
        context['invoice_lines'] = InvoiceLine.objects.filter(invoice=context['invoice'][0])

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

        context['job_site_id'] = self.object.pk
        context['jobsite'] = ViewJobSiteForm(instance=JobSite.objects.get(pk=context['job_site_id']), prefix='job')
        context['all_job_sites'] = JobSite.objects.filter(customer=self.object.customer)

        context['existing_equipment'] = JobSiteEquipment.objects.filter(job_site=context['job_site_id'])
        context['all_equipment'] = Equipment.objects.all()
        context['add_equipment_form'] = AddJobSiteEquipment(prefix='equipment')

        context['current_date'] = datetime.now()

        return context


class ViewDeleteEquipmentFromJobSite(LoginRequiredMixin, generic.DeleteView):
    model = JobSiteEquipment
    template_name = 'customer/view_customer/job_site.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return HttpResponse('success')


class ViewEditEquipmentLine(LoginRequiredMixin, generic.UpdateView):
    model = JobSiteEquipment
    template_name = 'customer/view_customer/edit_equipment_line.html'
    form_class = EditJobSiteEquipment

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['equipment_line_id'] = self.object.pk
        return context


class AddJobSiteToCustomer(LoginRequiredMixin, generic.CreateView):
    model = JobSite
    template_name = 'customer/view_customer/job_site_form.html'
    form_class = AddJobSiteForm
    form2 = AddJobSiteForm(prefix='jstc')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form2'] = self.form2
        return context


class SaveJobSiteToCustomer(LoginRequiredMixin, generic.CreateView):
    model = JobSite
    template_name = 'customer/view_customer/job_site_form.html'
    form_class = AddJobSiteForm

    def post(self, request, *args, **kwargs):
        print(request.POST)
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
    template_name = 'customer/view_customer/job_site_form.html'
    form_class = ViewJobSiteForm

    def post(self, request, *args, **kwargs):
        job_site = JobSite.objects.get(pk=self.kwargs['pk'])
        job_site_form = AddJobSiteForm(request.POST, instance=job_site, prefix='job')

        if job_site_form.is_valid():
            job_site_form.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
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
    template_name = 'customer/view_customer/edit_equipment_line.html'
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
    template_name = 'customer/view_customer/add_equipment_jobsite.html'
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
