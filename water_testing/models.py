from django.db import models
from customer.models import JobSite


class WaterTestType(models.Model):
    name = models.CharField(max_length=200)
    created_on = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Water Test Type'
        verbose_name_plural = 'Water Test Types'


class WaterTest(models.Model):
    sample_date = models.DateTimeField()
    sample_address = models.TextField()
    sample_point = models.CharField(max_length=200)
    job_site = models.ForeignKey(JobSite, on_delete=models.CASCADE, blank=True, null=True)
    type = models.ForeignKey(WaterTestType, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Water Test'
        verbose_name_plural = 'Water Tests'
