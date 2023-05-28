# authentication/serializers.py
from django.contrib.auth.models import Group
from rest_framework import serializers
from .models import Employee
from django.utils import timezone


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('name',)


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={'input_type': 'password'})
    groups = GroupSerializer(many=True, read_only=True)

    class Meta:
        model = Employee
        fields = ['id', 'email', 'password', 'first_name', 'last_name', 'role',
                  'groups', 'is_staff', 'is_superuser', 'date_joined']
        read_only_fields = ['is_staff', 'groups']
        extra_kwargs = {
            'password': {'write_only': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
            'date_joined': {'default': timezone.now, 'format': '%d %B %Y %H:%M'}
        }
    # date_joined = serializers.DateTimeField(default=timezone.now, format='%d %B %Y %H:%M')

    def validate(self, data):
        """
            Check that email ends with @epicevents.com
        """
        if not data['email'].endswith('@epicevents.com'):
            raise serializers.ValidationError(
                "Wrong email format: Please make sure to write @epicevents.com")
        return data

    def create(self, validated_data):
        return Employee.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """
            Update an employee.
        """
        instance.set_password(validated_data['password'])
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.role = validated_data.get('role', instance.role)
        instance.is_superuser = validated_data.get('is_superuser', instance.is_superuser)

        instance.save()
        return instance
