from django.views import generic
from .models import Customer
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from .forms import AddCustomerForm, ViewCustomerForm
from django.utils import timezone
from datetime import datetime, timedelta
from django.contrib.auth.mixins import LoginRequiredMixin


class AllCustomers(LoginRequiredMixin, generic.ListView):
    model = Customer
    queryset = Customer.objects.all()
    template_name = 'customer/all_customers.html'


class CustomersDueThisMonth(LoginRequiredMixin, generic.ListView):
    model = Customer
    queryset = Customer.objects.filter(next_service__month=timezone.now().month)\
        .filter(next_service__year=timezone.now().year).filter(is_active=True)
    template_name = 'customer/reports/due_this_month.html'


class CustomersDueNextMonth(LoginRequiredMixin, generic.ListView):
    model = Customer
    queryset = Customer.objects.filter(next_service__month=(timezone.now().month + 1))\
        .filter(next_service__year=timezone.now().year).filter(is_active=True)
    template_name = 'customer/reports/due_next_month.html'


class CustomersDueTwoMonthsFuture(LoginRequiredMixin, generic.ListView):
    model = Customer
    queryset = Customer.objects.filter(next_service__month=(timezone.now().month + 2))\
        .filter(next_service__year=timezone.now().year).filter(is_active=True)
    template_name = 'customer/reports/due_two_months_future.html'


class CustomersDueLastMonth(LoginRequiredMixin, generic.ListView):
    model = Customer
    queryset = Customer.objects.filter(next_service__month=(timezone.now().month - 1))\
        .filter(next_service__year=timezone.now().year).filter(is_active=True)
    template_name = 'customer/reports/due_last_month.html'


class CustomersDueLastThreeMonths(LoginRequiredMixin, generic.ListView):
    model = Customer
    queryset = Customer.objects.filter(next_service__gt=(datetime.now() - timedelta(weeks=12)))\
        .filter(next_service__lt=timezone.now()).filter(next_service__year=timezone.now().year).filter(is_active=True)
    template_name = 'customer/reports/due_last_three_months.html'


class CustomersDueLastYearThisMonth(LoginRequiredMixin, generic.ListView):
    model = Customer
    queryset = Customer.objects.filter(next_service__month=timezone.now().month)\
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


class ViewCustomer(LoginRequiredMixin, generic.UpdateView):
    model = Customer
    template_name = 'customer/view_customer.html'
    form_class = ViewCustomerForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            Customer.objects.filter(pk=kwargs['pk']).update(**form.cleaned_data)
            return HttpResponseRedirect('/')
        else:
            return HttpResponseBadRequest('Unable to update the customer.')
