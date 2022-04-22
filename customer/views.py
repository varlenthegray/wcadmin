from django.views import generic
from .models import Customer


# Create your views here.
class AllCustomers(generic.ListView):
    model = Customer
    queryset = Customer.objects.all()
    template_name = 'customer/all_customers.html'


class AddCustomer(generic.CreateView):
    model = Customer
    fields = ['company', 'title', 'first_name', 'middle_name', 'last_name', 'secondary_contact_name', 'website',
              'email', 'main_phone', 'alternate_phone', 'fax_number', 'billing_address_1', 'billing_address_2',
              'billing_address_3', 'billing_address_4', 'billing_city', 'billing_state', 'billing_zip',
              'jobsite_address_1', 'jobsite_address_2', 'jobsite_address_3', 'jobsite_address_4', 'jobsite_city',
              'jobsite_state', 'jobsite_zip', 'access_code', 'next_service', 'service_interval', 'is_active',
              'requires_supporting_technician']
    template_name = 'customer/add_customer.html'

    def form_valid(self, form):
        Customer.objects.create(form.cleaned_data)
        return super().form_valid(form)
