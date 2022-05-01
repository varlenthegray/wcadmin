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
    email = models.EmailField()
    main_phone = models.CharField(max_length=15)
    alternate_phone = models.CharField(max_length=15, null=True, blank=True)
    fax_number = models.CharField(max_length=15, null=True, blank=True)
    billing_address_same_as_jobsite = models.BooleanField(default=False, null=True, blank=True)
    billing_address_1 = models.CharField(max_length=200, null=True, blank=True)
    billing_address_2 = models.CharField(max_length=200, null=True, blank=True)
    billing_address_3 = models.CharField(max_length=200, null=True, blank=True)
    billing_address_4 = models.CharField(max_length=200, null=True, blank=True)
    billing_city = models.CharField(max_length=100, null=True, blank=True)
    billing_state = models.CharField(max_length=2, null=True, blank=True)
    billing_zip = models.CharField(max_length=10, null=True, blank=True)
    jobsite_address_1 = models.CharField(max_length=200, null=True, blank=True)
    jobsite_address_2 = models.CharField(max_length=200, null=True, blank=True)
    jobsite_address_3 = models.CharField(max_length=200, null=True, blank=True)
    jobsite_address_4 = models.CharField(max_length=200, null=True, blank=True)
    jobsite_city = models.CharField(max_length=200, null=True, blank=True)
    jobsite_state = models.CharField(max_length=2, null=True, blank=True)
    jobsite_zip = models.CharField(max_length=10, null=True, blank=True)
    access_code = models.CharField(max_length=20, null=True, blank=True)
    next_service = models.DateField(null=True, blank=True)
    service_interval = models.IntegerField(default=12)
    is_active = models.BooleanField(default=True)
    requires_supporting_technician = models.BooleanField(default=False)
    primary_technician = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return "%s %s" % (self.first_name, self.last_name)


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
