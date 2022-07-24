from django import forms
from django.contrib.auth.models import User
from django.forms import ModelMultipleChoiceField
from .models import EmailHistory, EmailTemplates
from customer.models import Customer


class SendField(ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        if obj.first_name:
            return f"{obj.first_name} {obj.last_name} <{obj.email}>"
        elif obj.company:
            return f"{obj.company} <{obj.email}>"
        else:
            return f"{obj.email}"


class CreateEmail(forms.ModelForm):
    send_to = SendField(queryset=Customer.objects.all().exclude(email=None)
                         .order_by('first_name', 'last_name', 'company', 'email'), required=False)
    send_cc = SendField(queryset=User.objects.all().exclude(email='')
                        .order_by('first_name', 'last_name', 'username'), required=False)
    template_used = forms.ModelChoiceField(queryset=EmailTemplates.objects.all(), required=False)

    class Meta:
        model = EmailHistory
        fields = ['send_to', 'send_cc', 'subject', 'message', 'template_used']


class CreateTemplate(forms.ModelForm):
    class Meta:
        model = EmailTemplates
        fields = ['template_name', 'subject', 'message']
