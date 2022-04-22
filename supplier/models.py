from django.db import models
from django.conf import settings


# Create your models here.
class Supplier(models.Model):
    contact_first_name = models.CharField(max_length=200)
    contact_last_name = models.CharField(max_length=200)
    company_name = models.CharField(max_length=200)
    support_email = models.EmailField()
    support_phone = models.CharField(max_length=15)
    sales_email = models.EmailField()
    sales_phone = models.CharField(max_length=15)
    csr_email = models.EmailField()
    csr_phone = models.CharField(max_length=15)
    website = models.CharField(max_length=150)
    have_1099 = models.BooleanField(default=False)
    billing_address_1 = models.CharField(max_length=200)
    billing_address_2 = models.CharField(max_length=200)
    billing_city = models.CharField(max_length=100)
    billing_state = models.CharField(max_length=2)
    billing_zip = models.CharField(max_length=10)
    is_active = models.BooleanField(default=True)
    terms = models.CharField(max_length=30)
    created_on = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated_on = models.DateTimeField(auto_now=True, editable=False)
    last_updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, editable=False)
