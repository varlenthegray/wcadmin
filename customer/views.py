from django.views import generic
from .models import Customer


# Create your views here.
class AllCustomers(generic.ListView):
    model = Customer
    queryset = Customer.objects.all()
    template_name = 'customer/all_customers.html'
