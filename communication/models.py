from django.db import models
from django.conf import settings


# Create your models here.
class EmailHistory(models.Model):
    send_to = models.TextField()
    send_from = models.CharField(max_length=200)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, editable=False)
    timestamp = models.DateTimeField(auto_now_add=True, editable=False)
