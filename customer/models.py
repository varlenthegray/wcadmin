import uuid
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from equipment.models import Equipment
from django.conf import settings


# Create your models here.
class Customer(models.Model):
    quickbooks_id = models.IntegerField(editable=False)
    company = models.CharField(max_length=100, null=True)
    title = models.CharField(max_length=30, null=True)
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100)
    secondary_contact_name = models.CharField(max_length=100, null=True)
    website = models.URLField(null=True)
    email = models.EmailField()
    main_phone = PhoneNumberField()
    alternate_phone = PhoneNumberField(null=True)
    fax_number = PhoneNumberField(null=True)
    billing_address_1 = models.CharField(max_length=200, null=True)
    billing_address_2 = models.CharField(max_length=200, null=True)
    billing_address_3 = models.CharField(max_length=200, null=True)
    billing_address_4 = models.CharField(max_length=200, null=True)
    billing_city = models.CharField(max_length=100, null=True)
    billing_state = models.CharField(max_length=2, null=True)
    billing_zip = models.CharField(max_length=10, null=True)
    jobsite_address_1 = models.CharField(max_length=200, null=True)
    jobsite_address_2 = models.CharField(max_length=200, null=True)
    jobsite_address_3 = models.CharField(max_length=200, null=True)
    jobsite_address_4 = models.CharField(max_length=200, null=True)
    jobsite_city = models.CharField(max_length=200, null=True)
    jobsite_state = models.CharField(max_length=2, null=True)
    jobsite_zip = models.CharField(max_length=10, null=True)
    access_code = models.CharField(max_length=20, null=True)
    next_service = models.DateField(null=True)
    service_interval = models.IntegerField(default=12)
    is_active = models.BooleanField(default=True)
    requires_supporting_technician = models.BooleanField(default=False)
    primary_technician = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)


class CustomerEquipment(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    installation_date = models.DateField()
    is_active = models.BooleanField(default=True)


class CustomerEquipmentPhotos(models.Model):
    customer_equipment = models.ForeignKey(CustomerEquipment, on_delete=models.CASCADE)
    photo = models.URLField()
    created_on = models.DateField(editable=False, auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, editable=False)


class CustomerNotesCategory(models.Model):
    category_name = models.CharField(max_length=100)


class CustomerNotes(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    category = models.ForeignKey(CustomerNotesCategory, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)
    timestamp = models.DateTimeField(editable=False, auto_now_add=True)
    note = models.TextField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, editable=False)
