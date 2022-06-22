from django import forms
from .models import EmailHistory


class CreateEmail(forms.ModelForm):
    class Meta:
        model = EmailHistory
        fields = ['send_bcc', 'send_cc', 'subject', 'message', 'template_used']
