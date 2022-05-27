from django.db import models
from jobsite.models import JobSite


class Invoice(models.Model):
    job_site = models.ForeignKey(JobSite, on_delete=models.CASCADE)
    invoice_num = models.IntegerField()
    invoice_date = models.CharField(max_length=10)
    total = models.FloatField(null=True, blank=True)
    memo = models.TextField(null=True, blank=True)
    service_interval = models.IntegerField(default=12)


class InvoiceLine(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    line_id = models.IntegerField()
    description = models.CharField(max_length=200)
    price = models.FloatField()
