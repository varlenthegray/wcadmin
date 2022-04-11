from django.core.paginator import Paginator
from django.shortcuts import render
from django.views import generic
from customer.models import Customer


class DashboardView(generic.ListView):
    model = Customer
    queryset = Customer.objects.all()
    paginate_by = 20
    template_name = "base.html"
