from django.db import models
from supplier.models import Supplier
from django.conf import settings


# Create your models here.
class Equipment(models.Model):
    sku = models.CharField(max_length=100, blank=True, null=True)
    name = models.CharField(max_length=100)
    url = models.URLField(blank=True, null=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, blank=True, null=True)
    cost = models.FloatField()
    default_image = models.URLField(blank=True, null=True)
    sales_price = models.FloatField()
    tags = models.CharField(max_length=512, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated_on = models.DateTimeField(auto_now=True, editable=False)
    last_updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, editable=False,
                                        default=settings.AUTH_USER_MODEL)

    def __str__(self):
        return "%s - %s" % (self.sku, self.name)
