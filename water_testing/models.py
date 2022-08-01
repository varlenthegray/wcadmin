from django.db import models
from django.conf import settings

from customer.models import JobSite


class WaterTestType(models.Model):
    name = models.CharField(max_length=200)
    created_on = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Water Test Type'
        verbose_name_plural = 'Water Test Types'


class WaterTestLineItem(models.Model):
    analyte = models.CharField(max_length=200)
    allowable_limit = models.CharField(max_length=50)
    unit = models.CharField(max_length=50)
    last_modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Water Test - Line Item'
        verbose_name_plural = 'Water Test - Line Items'


class WaterTest(models.Model):
    sample_date = models.DateTimeField()
    sample_address = models.TextField()
    sample_point = models.CharField(max_length=200)
    job_site = models.ForeignKey(JobSite, on_delete=models.CASCADE, blank=True, null=True)
    type = models.ForeignKey(WaterTestType, on_delete=models.CASCADE)
    line_items = models.ManyToManyField(WaterTestLineItem)

    class Meta:
        verbose_name = 'Water Test'
        verbose_name_plural = 'Water Tests'
