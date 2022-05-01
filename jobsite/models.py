from django.db import models
from django.conf import settings
from customer.models import Customer


class JobSite(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=2)
    zip = models.CharField(max_length=10)
    phone_number = models.CharField(max_length=20)
    email = models.CharField(max_length=200)
    service_interval = models.IntegerField(default=12)
    next_service_date = models.DateField()
    primary_technician = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    active = models.BooleanField(default=True)
    access_code = models.CharField(max_length=10)
    bill_parent = models.BooleanField(default=False)
    requires_supporting_technician = models.BooleanField(default=False)
