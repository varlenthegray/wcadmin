from django.db import models
from customer.models import JobSite
from equipment.models import Equipment
from django.conf import settings


class Invoice(models.Model):
    job_site = models.ForeignKey(JobSite, on_delete=models.CASCADE)
    invoice_num = models.CharField(max_length=50)
    invoice_date = models.DateField()
    total = models.FloatField(null=True, blank=True)
    memo = models.TextField(null=True, blank=True)
    service_interval = models.IntegerField(default=12)

    class Meta:
        verbose_name = 'Invoice'
        verbose_name_plural = 'Invoices'

    def __str__(self):
        return f"#{self.invoice_num}"


class InvoiceLine(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    line_id = models.IntegerField()
    description = models.TextField()
    price = models.FloatField()
    quantity = models.IntegerField(default=1)
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        verbose_name = 'Invoice Line'
        verbose_name_plural = 'Invoice Lines'

    def __str__(self):
        return f"{self.equipment.name}"


class QBSystem(models.Model):
    last_update = models.DateTimeField(blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, editable=False)

    def __str__(self):
        return f"{self.user} @ {self.last_update}"

    class Meta:
        verbose_name = 'QuickBooks System'
        verbose_name_plural = 'QuickBooks System'
