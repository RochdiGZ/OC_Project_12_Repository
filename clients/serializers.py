from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import Client, Contract, ContractStatus, Event


class ClientSerializer(ModelSerializer):
    sales_contact = serializers.ReadOnlyField(
        source='sales_contact.email', read_only=False)

    class Meta:
        model = Client
        fields = ['id', 'first_name', 'last_name', 'email', 'phone', 'mobile',
                  'company_name', 'is_prospect', 'sales_contact', ]


class ContractSerializer(ModelSerializer):
    sales_contact = serializers.ReadOnlyField(source='sales_contact.email', read_only=True)

    class Meta:
        model = Contract
        fields = ('id', 'amount', 'payment_due', 'status', 'date_created', 'date_updated', 'client', 'sales_contact', )
        read_only_fields = ('id', 'status', 'date_created', 'date_updated',)


class UpdateContractSerializer(ModelSerializer):
    sales_contact = serializers.ReadOnlyField(source='sales_contact.email', read_only=True)

    class Meta:
        model = Contract
        fields = ('id', 'amount', 'payment_due', 'status', 'date_created', 'date_updated', 'client', 'sales_contact', )
        read_only_fields = ('id', 'client', 'sales_contact', 'date_created', 'date_updated',)


class ContractStatusSerializer(ModelSerializer):
    class Meta:
        model = ContractStatus
        fields = "__all__"


class PartialEventSerializer(serializers.ModelSerializer):
    client = serializers.ReadOnlyField(source='client.company_name', read_only=True)
    support_contact = serializers.ReadOnlyField(source='support_contact.email', read_only=True)

    class Meta:
        model = Event
        fields = "__all__"
        read_only_fields = ('id', 'support_contact', 'date_created', 'date_updated',)


class AllEventSerializer(serializers.ModelSerializer):
    client = serializers.ReadOnlyField(source='client.company_name', read_only=True)
    support_contact = serializers.ReadOnlyField(source='support_contact.email', read_only=True)

    class Meta:
        model = Event
        fields = "__all__"
