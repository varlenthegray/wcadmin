from django.db import models
from django.conf import settings
from customer.models import Customer, Equipment


class JobSite(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    quickbooks_id = models.IntegerField(editable=False, null=True, blank=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    address_2 = models.CharField(max_length=200, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=50, null=True, blank=True)
    zip = models.CharField(max_length=20, null=True, blank=True)
    phone_number = models.CharField(max_length=30, null=True, blank=True)
    email = models.CharField(max_length=400, null=True, blank=True)
    service_interval = models.IntegerField(default=12)
    next_service_date = models.DateField(null=True, blank=True)
    primary_technician = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    active = models.BooleanField(default=True)
    access_code = models.CharField(max_length=10, null=True, blank=True)
    bill_parent = models.BooleanField(default=False)
    requires_supporting_technician = models.BooleanField(default=False)
    service_scheduled = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.name}'


class JobSiteEquipment(models.Model):
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    job_site = models.ForeignKey(JobSite, on_delete=models.CASCADE)
    tags = models.CharField(max_length=512, blank=True, null=True)
    added_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, editable=False)
    installed_on = models.DateField(blank=True, null=True)

    def tags_as_list(self):
        return self.tags.split(',')

    def __str__(self):
        return f'{self.job_site.name} ({self.equipment})'
