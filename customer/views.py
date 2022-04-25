from django.views import generic
from .models import Customer
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from .forms import AddCustomerForm, ViewCustomerForm
from django.utils import timezone
from datetime import datetime, timedelta


class AllCustomers(generic.ListView):
    model = Customer
    queryset = Customer.objects.all()
    template_name = 'customer/all_customers.html'


class CustomersDueThisMonth(generic.ListView):
    model = Customer
    queryset = Customer.objects.filter(next_service__month=timezone.now().month)\
        .filter(next_service__year=timezone.now().year)
    template_name = 'customer/reports/due_this_month.html'


class CustomersDueNextMonth(generic.ListView):
    model = Customer
    queryset = Customer.objects.filter(next_service__month=(timezone.now().month + 1))\
        .filter(next_service__year=timezone.now().year)
    template_name = 'customer/reports/due_next_month.html'


class CustomersDueTwoMonthsFuture(generic.ListView):
    model = Customer
    queryset = Customer.objects.filter(next_service__month=(timezone.now().month + 2))\
        .filter(next_service__year=timezone.now().year)
    template_name = 'customer/reports/due_two_months_future.html'


class CustomersDueLastMonth(generic.ListView):
    model = Customer
    queryset = Customer.objects.filter(next_service__month=(timezone.now().month - 1))\
        .filter(next_service__year=timezone.now().year)
    template_name = 'customer/reports/due_last_month.html'


class CustomersDueLastThreeMonths(generic.ListView):
    model = Customer
    queryset = Customer.objects.filter(next_service__gt=(datetime.now() - timedelta(weeks=12)))\
        .filter(next_service__lt=timezone.now()).filter(next_service__year=timezone.now().year)
    template_name = 'customer/reports/due_last_three_months.html'


class CustomersCustomReport(generic.ListView):
    model = Customer
    queryset = Customer.objects.filter(next_service__month=timezone.now().month)\
        .filter(next_service__year=timezone.now().year)
    template_name = 'customer/reports/custom_report.html'


class AddCustomer(generic.CreateView):
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


class ViewCustomer(generic.UpdateView):
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
