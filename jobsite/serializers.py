from rest_framework import serializers
from .models import JobSite


class JobSitesSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = JobSite
        fields = ('id', 'quickbooks_id', 'name', 'address', 'address_2', 'city', 'state', 'zip', 'phone_number',
                  'email', 'next_service_date', 'service_scheduled')

        datatables_always_serialize = ('id', 'quickbooks_id', 'name', 'address', 'address_2', 'city', 'state', 'zip', 'phone_number',
                  'email', 'next_service_date', 'service_scheduled')
