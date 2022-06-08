from django.db import models
from equipment.models import Equipment
from django.conf import settings


# Create your models here.
class Customer(models.Model):
    quickbooks_id = models.IntegerField(editable=False, null=True, blank=True)
    company = models.CharField(max_length=100, null=True, blank=True)
    title = models.CharField(max_length=30, null=True, blank=True)
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100)
    secondary_contact_name = models.CharField(max_length=100, null=True, blank=True)
    website = models.URLField(null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    main_phone = models.CharField(max_length=30, null=True, blank=True)
    alternate_phone = models.CharField(max_length=30, null=True, blank=True)
    fax_number = models.CharField(max_length=30, null=True, blank=True)
    billing_address_same_as_jobsite = models.BooleanField(default=False, null=True, blank=True)
    billing_address_1 = models.CharField(max_length=200, null=True, blank=True)
    billing_address_2 = models.CharField(max_length=200, null=True, blank=True)
    billing_city = models.CharField(max_length=100, null=True, blank=True)
    billing_state = models.CharField(max_length=50, null=True, blank=True)
    billing_zip = models.CharField(max_length=20, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class CustomerNotes(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)
    timestamp = models.DateTimeField(editable=False, auto_now_add=True)
    note = models.TextField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, editable=False)
