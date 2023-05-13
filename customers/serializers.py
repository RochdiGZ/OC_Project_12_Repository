from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import Customer


class CustomerSerializer(ModelSerializer):
    sales_contact = serializers.ReadOnlyField(
        source='sales_contact.email', read_only=False)

    class Meta:
        model = Customer
        fields = ['id', 'first_name', 'last_name', 'email', 'phone', 'mobile',
                  'company_name', 'is_prospect', 'sales_contact', ]
