from django.db import models
from django.conf import settings


class EmailTemplates(models.Model):
    template_name = models.CharField(max_length=200)
    subject = models.CharField(max_length=200)
    send_cc = models.TextField(blank=True, null=True)
    message = models.TextField()
    last_updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, editable=False)
    last_updated_on = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        ordering = ['-last_updated_on']


class EmailHistory(models.Model):
    send_bcc = models.TextField(blank=True, null=True)
    send_cc = models.TextField(blank=True, null=True)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    template_used = models.ForeignKey(EmailTemplates, on_delete=models.CASCADE, blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, editable=False)
    status = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        ordering = ['-timestamp']
