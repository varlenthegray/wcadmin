from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.views import generic
from .models import Customer
from jobsite.models import JobSite
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from .forms import AddCustomerForm, ViewCustomerForm, ViewJobSiteForm
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
    job_site = JobSite.objects.filter(customer=pk).first()
    all_job_sites = JobSite.objects.filter(customer=pk)
    edit_customer = ViewCustomerForm(instance=customer)
    edit_job_site = ViewJobSiteForm(instance=job_site)

    if request.method == 'POST':
        pass

    if job_site:
        jspk = job_site.pk
    else:
        jspk = 0

    context = {
        'form': edit_customer,
        'form2': edit_job_site,
        'all_job_sites': all_job_sites,
        'job_site_id': jspk
    }

    return render(request, 'customer/view_customer.html', context=context)


class ViewSpecificJobSite(LoginRequiredMixin, generic.UpdateView):
    model = JobSite
    template_name = 'customer/view_customer/job_site.html'
    form_class = ViewJobSiteForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form2'] = ViewJobSiteForm(instance=JobSite.objects.get(pk=self.object.pk))
        context['job_site_id'] = self.object.pk
        context['all_job_sites'] = JobSite.objects.filter(customer=self.object.customer)
        return context
