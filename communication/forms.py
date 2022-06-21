from django import forms
from .models import EmailHistory


class CreateEmail(forms.ModelForm):
    class Meta:
        model = EmailHistory
        fields = ['send_to', 'send_from', 'subject', 'message']