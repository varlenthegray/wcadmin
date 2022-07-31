from django.contrib.auth.models import User
from django.db import models
from django.conf import settings
from customer.models import Customer


class EmailTemplates(models.Model):
    template_name = models.CharField(max_length=200)
    subject = models.CharField(max_length=200)
    send_cc = models.TextField(blank=True, null=True)
    message = models.TextField()
    last_updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, editable=False)
    last_updated_on = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        ordering = ['-last_updated_on']
        verbose_name = 'Email Template'
        verbose_name_plural = 'Email Templates'

    def __str__(self):
        return f'{self.template_name}'


class EmailHistory(models.Model):
    send_to = models.ManyToManyField(Customer, blank=True, related_name='send_to')
    send_cc = models.ManyToManyField(User, blank=True, related_name='send_cc')
    subject = models.CharField(max_length=200)
    message = models.TextField()
    template_used = models.ForeignKey(EmailTemplates, on_delete=models.CASCADE, blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, editable=False)
    status = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'Email History'
        verbose_name_plural = 'All Email History'

    def __str__(self):
        return f'{self.subject}'

    @property
    def to_as_comma(self):
        all_to = ''

        for customer in self.send_to.all():
            all_to += customer.email

            if self.send_to.count() > 1:
                all_to += ', '

        if self.send_to.count() > 1:
            return all_to[:-2]
        else:
            return all_to

    @property
    def cc_as_comma(self):
        all_cc = ''

        for customer in self.send_cc.all():
            all_cc += customer.email

            if self.send_cc.count() > 1:
                all_cc += ', '

        if self.send_cc.count() > 1:
            return all_cc[:-2]
        else:
            return all_cc
