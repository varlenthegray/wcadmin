from django import forms
from .models import JobSite


class ViewJobSiteForm(forms.ModelForm):
    class Meta:
        model = JobSite
        fields = ['name', 'address', 'city', 'state', 'zip', 'phone_number', 'email', 'next_service_date', 'active',
                  'access_code', 'bill_parent', 'customer', 'primary_technician', 'service_interval',
                  'requires_supporting_technician']
