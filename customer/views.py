from django.shortcuts import render
from .models import Customer


# Create your views here.
def all_customers(request):
    return render(request, 'base.html')
