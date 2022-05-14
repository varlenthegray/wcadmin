from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.views import generic
from .models import Customer
from jobsite.models import JobSite, JobSiteEquipment
from equipment.models import Equipment
from django.http import HttpResponseRedirect, HttpResponseBadRequest, HttpResponse
from .forms import AddCustomerForm, ViewCustomerForm, ViewJobSiteForm, EditJobSiteEquipment, AddJobSiteEquipment, AddJobSiteForm
from django.utils import timezone
from datetime import datetime, timedelta
from django.contrib.auth.mixins import LoginRequiredMixin


class AllCustomers(LoginRequiredMixin, generic.ListView):
    model = Customer
    queryset = Customer.objects.all()
    template_name = 'customer/all_customers.html'


class CustomersDueThisMonth(LoginRequiredMixin, generic.ListView):
    model = Customer
    queryset = Customer.objects.filter(next_service__month=timezone.now().month) \
        .filter(next_service__year=timezone.now().year).filter(is_active=True)
    template_name = 'customer/reports/due_this_month.html'


class CustomersDueNextMonth(LoginRequiredMixin, generic.ListView):
    model = Customer
    queryset = Customer.objects.filter(next_service__month=(timezone.now().month + 1)) \
        .filter(next_service__year=timezone.now().year).filter(is_active=True)
    template_name = 'customer/reports/due_next_month.html'


class CustomersDueTwoMonthsFuture(LoginRequiredMixin, generic.ListView):
    model = Customer
    queryset = Customer.objects.filter(next_service__month=(timezone.now().month + 2)) \
        .filter(next_service__year=timezone.now().year).filter(is_active=True)
    template_name = 'customer/reports/due_two_months_future.html'


class CustomersDueLastMonth(LoginRequiredMixin, generic.ListView):
    model = Customer
    queryset = Customer.objects.filter(next_service__month=(timezone.now().month - 1)) \
        .filter(next_service__year=timezone.now().year).filter(is_active=True)
    template_name = 'customer/reports/due_last_month.html'


class CustomersDueLastThreeMonths(LoginRequiredMixin, generic.ListView):
    model = Customer
    queryset = Customer.objects.filter(next_service__gt=(datetime.now() - timedelta(weeks=12))) \
        .filter(next_service__lt=timezone.now()).filter(next_service__year=timezone.now().year).filter(is_active=True)
    template_name = 'customer/reports/due_last_three_months.html'


class CustomersDueLastYearThisMonth(LoginRequiredMixin, generic.ListView):
    model = Customer
    queryset = Customer.objects.filter(next_service__month=timezone.now().month) \
        .filter(next_service__year=(timezone.now().year - 1)).filter(is_active=True)
    template_name = 'customer/reports/due_last_year_this_month.html'


class CustomersCustomReport(LoginRequiredMixin, generic.ListView):
    model = Customer
    template_name = 'customer/reports/custom_report.html'

    def get_queryset(self):
        from_date = self.request.GET.get('fromDate')
        to_date = self.request.GET.get('toDate')
        self.queryset = Customer.objects.filter(is_active=True)

        if from_date:
            from_date = datetime.strptime(from_date, '%m-%d-%Y').strftime('%Y-%m-%d')
            print("Checking date from " + from_date)

            self.queryset = self.queryset.filter(next_service__gte=from_date)

        if to_date:
            to_date = datetime.strptime(to_date, '%m-%d-%Y').strftime('%Y-%m-%d')
            print("Checking date to " + to_date)
            self.queryset = self.queryset.filter(next_service__lte=to_date)

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


@login_required
def view_customer(request, pk):
    customer = get_object_or_404(Customer, id=pk)
    customer_id = pk
    job_site = JobSite.objects.filter(customer=pk).first()
    all_job_sites = JobSite.objects.filter(customer=pk)
    edit_customer = ViewCustomerForm(instance=customer, prefix='customer')
    edit_job_site = ViewJobSiteForm(instance=job_site, prefix='job')
    add_equipment_job_site = AddJobSiteEquipment(prefix='equipment')

    if request.method == 'POST':
        if 'customer-edit_customer' in request.POST:
            edit_customer = ViewCustomerForm(request.POST, instance=customer, prefix='customer')

            if edit_customer.is_valid():
                edit_customer.save()
            else:
                return HttpResponseBadRequest(edit_customer.errors)

        if 'job-edit_job_site' in request.POST:
            current_job_site = JobSite.objects.get(pk=request.POST['job_id'])
            edit_job_site = ViewJobSiteForm(request.POST, instance=current_job_site, prefix='job')

            if edit_job_site.is_valid():
                edit_job_site.save()
            else:
                return HttpResponseBadRequest(edit_job_site.errors)

        if 'edit_job_site_equipment' in request.POST:
            job_site_equipment_line = JobSiteEquipment.objects.get(pk=request.POST['equipment_line_id'])
            edit_job_site_equipment = EditJobSiteEquipment(request.POST, instance=job_site_equipment_line)

            if edit_job_site_equipment.is_valid():
                edit_job_site_equipment.save()
            else:
                return HttpResponseBadRequest(edit_job_site_equipment.errors)

    if job_site:
        jspk = job_site.pk
    else:
        jspk = 0

    existing_equipment = JobSiteEquipment.objects.filter(job_site=jspk)

    context = {
        'customer_id': customer_id,
        'form': edit_customer,
        'form2': edit_job_site,
        'all_job_sites': all_job_sites,
        'job_site_id': jspk,
        'existing_equipment': existing_equipment,
        'all_equipment': Equipment.objects.all(),
        'add_equipment_form': add_equipment_job_site,
    }

    return render(request, 'customer/view_customer.html', context=context)


class ViewSpecificJobSite(LoginRequiredMixin, generic.UpdateView):
    model = JobSite
    template_name = 'customer/view_customer/job_site.html'
    form_class = ViewJobSiteForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['job_site_id'] = self.object.pk
        context['form2'] = ViewJobSiteForm(instance=JobSite.objects.get(pk=context['job_site_id']))
        context['all_job_sites'] = JobSite.objects.filter(customer=self.object.customer)
        context['existing_equipment'] = JobSiteEquipment.objects.filter(job_site=context['job_site_id'])
        context['all_equipment'] = Equipment.objects.all()
        context['add_equipment_form'] = AddJobSiteEquipment(prefix='equipment')
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
    form2 = AddJobSiteForm

    def post(self, request, *args, **kwargs):
        add_job_site_customer = AddJobSiteForm(request.POST, prefix='job')

        if add_job_site_customer.is_valid():
            print("Saving job site to customer")
            return HttpResponse(status=200)
        else:
            print("Unable to save job site to customer")
            return HttpResponseBadRequest(add_job_site_customer.errors)


class AddEquipmentToJobSite(LoginRequiredMixin, generic.CreateView):
    model = JobSiteEquipment
    template_name = 'customer/view_customer/add_equipment_jobsite.html'
    form_class = AddJobSiteEquipment

    def post(self, request, *args, **kwargs):
        jobsite = JobSite.objects.get(pk=request.POST['job_id'])
        add_equipment_jobsite = AddJobSiteEquipment(request.POST, instance=jobsite, prefix='equipment')

        if add_equipment_jobsite.is_valid():
            data = add_equipment_jobsite.cleaned_data
            JobSiteEquipment.objects.create(
                tags=data['tags'],
                installed_on=data['installed_on'],
                added_by=request.user,
                equipment=data['equipment'],
                job_site=jobsite
            )

            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            return HttpResponseBadRequest(add_equipment_jobsite.errors)
