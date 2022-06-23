from django import forms
from .models import EmailHistory, EmailTemplates


class CreateEmail(forms.ModelForm):
    class Meta:
        model = EmailHistory
        fields = ['send_bcc', 'send_cc', 'subject', 'message', 'template_used']


class CreateTemplate(forms.ModelForm):
    class Meta:
        model = EmailTemplates
        fields = ['template_name', 'subject', 'send_cc', 'message']
