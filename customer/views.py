from django.views import generic
from .models import Customer
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from .forms import AddCustomerForm, ViewCustomerForm


# Create your views here.
class AllCustomers(generic.ListView):
    model = Customer
    queryset = Customer.objects.all()
    template_name = 'customer/all_customers.html'


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
