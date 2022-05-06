from django import forms
from .models import Customer
from jobsite.models import JobSite


class AddCustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['company', 'title', 'first_name', 'middle_name', 'last_name', 'secondary_contact_name', 'website',
                  'email', 'main_phone', 'alternate_phone', 'fax_number', 'billing_address_1', 'billing_city',
                  'billing_state', 'billing_zip']


class ViewCustomerForm(forms.ModelForm):
    next_service = forms.DateField(widget=forms.DateInput(format='%m-%d-%Y'), input_formats=['%m-%d-%Y'])
    edit_customer = forms.BooleanField(widget=forms.HiddenInput, initial=True)

    class Meta:
        model = Customer
        fields = ['company', 'title', 'first_name', 'middle_name', 'last_name', 'secondary_contact_name', 'website',
                  'email', 'main_phone', 'alternate_phone', 'fax_number', 'billing_address_1', 'billing_city',
                  'billing_state', 'billing_zip']


class ViewJobSiteForm(forms.ModelForm):
    edit_job_site = forms.BooleanField(widget=forms.HiddenInput, initial=True)

    class Meta:
        model = JobSite
        fields = ['name', 'address', 'city', 'state', 'zip', 'phone_number', 'email', 'next_service_date', 'active',
                  'access_code', 'bill_parent', 'customer', 'primary_technician', 'service_interval',
                  'requires_supporting_technician']
