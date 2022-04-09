from django.db import models
from customer.models import Customer
from django.conf import settings


# Create your models here.
class ServiceReason(models.Model):
    type = models.CharField(max_length=100)


class ServiceRecord(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    notes = models.TextField()
    service_reason = models.ForeignKey(ServiceReason, on_delete=models.CASCADE)
    service_date = models.DateField()
    created_on = models.DateTimeField(editable=False, auto_now_add=True)
    last_updated_on = models.DateTimeField(editable=False, auto_now=True)
    last_updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, editable=False)


class ServicePicture(models.Model):
    service_record = models.ForeignKey(ServiceRecord, on_delete=models.CASCADE)
    image = models.URLField()
    is_archived = models.BooleanField(default=False)
    created_on = models.DateTimeField(editable=False, auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, editable=False)
