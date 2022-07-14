from dateutil.relativedelta import relativedelta
from django.db import models
from django.utils import timezone

from equipment.models import Equipment
from django.conf import settings


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
    notes = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    qb_created_on = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class CustomerNotes(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, blank=True)
    subject = models.CharField(max_length=100)
    timestamp = models.DateTimeField(editable=False, auto_now=True)
    note = models.TextField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True)


class JobSite(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    quickbooks_id = models.IntegerField(editable=False, null=True, blank=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    first_name = models.CharField(max_length=200, null=True, blank=True)
    last_name = models.CharField(max_length=200, null=True, blank=True)
    print_on_check_name = models.CharField(max_length=200, null=True, blank=True)
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
    disable_service = models.BooleanField(default=False)
    qb_created_on = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'{self.name}'

    @property
    def is_past_due(self):
        ignore_after = timezone.localdate() - relativedelta(years=5)

        # noinspection StrFormat
        if self.next_service_date:
            if ignore_after >= self.next_service_date:
                return False
            else:
                return timezone.localdate() > self.next_service_date
        else:
            return False

    @property
    def is_due_soon(self):
        ignore_after = timezone.localdate() - relativedelta(years=3)

        if self.next_service_date and self.next_service_date >= ignore_after:
            three_months_future = timezone.localdate() + relativedelta(months=2)
            return three_months_future > self.next_service_date
        else:
            return False


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
