from django import forms
from .models import Customer


class AddCustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['company', 'title', 'first_name', 'middle_name', 'last_name', 'secondary_contact_name', 'website',
                  'email', 'main_phone', 'alternate_phone', 'fax_number', 'billing_address_1', 'billing_city',
                  'billing_state', 'billing_zip', 'jobsite_address_1', 'jobsite_city', 'jobsite_state', 'jobsite_zip',
                  'access_code']


class ViewCustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['company', 'title', 'first_name', 'middle_name', 'last_name', 'secondary_contact_name', 'website',
                  'email', 'main_phone', 'alternate_phone', 'fax_number', 'billing_address_1', 'billing_city',
                  'billing_state', 'billing_zip', 'jobsite_address_1', 'jobsite_city', 'jobsite_state', 'jobsite_zip',
                  'access_code']
