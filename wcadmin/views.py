from datetime import datetime, timedelta
from django.views import generic
from customer.models import Customer


class DashboardView(generic.ListView):
    model = Customer
    queryset = Customer.objects.filter(next_service__range=[datetime.today(), datetime.today() + timedelta(days=30)])
    template_name = "base.html"
