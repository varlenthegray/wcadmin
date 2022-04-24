from django import forms
from .models import Customer


class AddCustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['company', 'title', 'first_name', 'middle_name', 'last_name', 'secondary_contact_name', 'website',
                  'email', 'main_phone', 'alternate_phone', 'fax_number', 'billing_address_1', 'billing_city',
                  'billing_state', 'billing_zip', 'jobsite_address_1', 'jobsite_city', 'jobsite_state', 'jobsite_zip',
                  'access_code', 'billing_address_same_as_jobsite']


class ViewCustomerForm(forms.ModelForm):
    next_service = forms.DateField(widget=forms.DateInput(format='%m-%d-%Y'), input_formats=['%m-%d-%Y'])

    class Meta:
        model = Customer
        fields = ['company', 'title', 'first_name', 'middle_name', 'last_name', 'secondary_contact_name', 'website',
                  'email', 'main_phone', 'alternate_phone', 'fax_number', 'billing_address_1', 'billing_city',
                  'billing_state', 'billing_zip', 'jobsite_address_1', 'jobsite_city', 'jobsite_state', 'jobsite_zip',
                  'access_code', 'billing_address_same_as_jobsite', 'next_service', 'service_interval', 'is_active',
                  'requires_supporting_technician', 'primary_technician']
