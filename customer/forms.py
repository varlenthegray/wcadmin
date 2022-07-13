from django import forms
from .models import Customer, JobSite, JobSiteEquipment
# from jobsite.models import JobSite, JobSiteEquipment


class AddCustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['company', 'title', 'first_name', 'middle_name', 'last_name', 'secondary_contact_name', 'website',
                  'email', 'main_phone', 'alternate_phone', 'fax_number', 'billing_address_1', 'billing_city',
                  'billing_state', 'billing_zip']


class ViewCustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['company', 'title', 'first_name', 'middle_name', 'last_name', 'secondary_contact_name', 'website',
                  'email', 'main_phone', 'alternate_phone', 'fax_number', 'billing_address_1', 'billing_address_2',
                  'billing_city', 'billing_state', 'billing_zip', 'is_active', 'notes']


class ViewJobSiteForm(forms.ModelForm):
    next_service_date = forms.DateField(widget=forms.DateInput(format='%m-%d-%Y'), input_formats=['%m-%d-%Y'])
    template_name = 'customer/view_customer/job_site_form.html'

    class Meta:
        model = JobSite
        fields = ['name', 'address', 'city', 'state', 'zip', 'phone_number', 'email', 'next_service_date',
                  'active', 'access_code', 'bill_parent', 'customer', 'primary_technician', 'service_interval',
                  'requires_supporting_technician', 'service_scheduled', 'disable_service']


class AddJobSiteForm(forms.ModelForm):
    next_service_date = forms.DateField(widget=forms.DateInput(format='%m-%d-%Y'), input_formats=['%m-%d-%Y'])
    template_name = 'customer/view_customer/job_site_form.html'

    class Meta:
        model = JobSite
        fields = ['name', 'address', 'city', 'state', 'zip', 'phone_number', 'email', 'next_service_date',
                  'active', 'access_code', 'bill_parent', 'service_interval', 'requires_supporting_technician',
                  'service_scheduled', 'disable_service']


class EditJobSiteEquipment(forms.ModelForm):
    installed_on = forms.DateField(widget=forms.DateInput(format='%m-%d-%Y'), input_formats=['%m-%d-%Y'])

    class Meta:
        model = JobSiteEquipment
        fields = ['tags', 'installed_on']


class AddJobSiteEquipment(forms.ModelForm):
    installed_on = forms.DateField(widget=forms.DateInput(format='%m-%d-%Y'), input_formats=['%m-%d-%Y'])

    class Meta:
        model = JobSiteEquipment
        fields = ['tags', 'installed_on', 'equipment']
