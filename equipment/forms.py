from django import forms
from .models import Equipment


class AddEquipmentForm(forms.ModelForm):
    class Meta:
        model = Equipment
        fields = ['sku', 'name', 'url', 'cost', 'default_image', 'sales_price', 'is_active']
