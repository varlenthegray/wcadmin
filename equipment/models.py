from django.db import models
from supplier.models import Supplier
from django.conf import settings


# Create your models here.
class Equipment(models.Model):
    sku = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    url = models.URLField()
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    cost = models.FloatField()
    default_image = models.URLField()
    sales_price = models.FloatField()
    is_active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated_on = models.DateTimeField(auto_now=True, editable=False)
    last_updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, editable=False)
