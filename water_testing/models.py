import secrets

from django.db import models
from django.conf import settings

from customer.models import JobSite


class ItemGroup(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = 'Item Group'
        verbose_name_plural = 'Item Groups'


class LineItem(models.Model):
    analyte = models.CharField(max_length=200)
    minimum_limit = models.FloatField()
    maximum_limit = models.FloatField()
    suggested_limit = models.BooleanField(default=False)
    unit = models.CharField(max_length=50)
    group = models.ForeignKey(ItemGroup, models.CASCADE, blank=True, null=True)
    last_modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.analyte}"

    class Meta:
        verbose_name = 'Line Item'
        verbose_name_plural = 'Line Items'
        ordering = ['group']


class Template(models.Model):
    name = models.CharField(max_length=200)
    line_items = models.ManyToManyField(LineItem, blank=True)
    created_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = 'Template'
        verbose_name_plural = 'Templates'


class WaterTest(models.Model):
    name = models.CharField(max_length=200)
    secondary_name = models.CharField(max_length=200, blank=True, null=True)
    sample_date = models.DateTimeField()
    sample_address = models.TextField()
    sample_point = models.CharField(max_length=200)
    job_site = models.ForeignKey(JobSite, on_delete=models.CASCADE, blank=True, null=True)
    token = models.CharField(max_length=32, editable=False, default=secrets.token_hex(4), unique=True)
    template = models.ForeignKey(Template, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f"{self.name}: {self.sample_address}"

    class Meta:
        verbose_name = 'Water Test'
        verbose_name_plural = 'Water Tests'


class LineResult(models.Model):
    line_item = models.ForeignKey(LineItem, on_delete=models.CASCADE)
    result = models.FloatField()
    added_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    water_test = models.ForeignKey(WaterTest, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.line_item} ({self.result})"

    class Meta:
        verbose_name = 'Line Result'
        verbose_name_plural = 'Line Results'
