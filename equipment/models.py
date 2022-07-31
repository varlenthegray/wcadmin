from django.db import models
from supplier.models import Supplier
from django.conf import settings


class Equipment(models.Model):
    quickbooks_id = models.IntegerField(blank=True, null=True)
    sku = models.CharField(max_length=100, blank=True, null=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    url = models.URLField(blank=True, null=True)

    cost = models.FloatField(blank=True, null=True)
    default_image = models.URLField(blank=True, null=True)
    sales_price = models.FloatField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated_on = models.DateTimeField(auto_now=True, editable=False)
    last_updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, editable=False)

    class Meta:
        ordering = ['name']
        verbose_name = 'Equipment'
        verbose_name_plural = 'All Equipment'

    def __str__(self):
        return f"{self.name}"
