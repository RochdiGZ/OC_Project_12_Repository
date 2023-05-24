# authentication/serializers.py
from rest_framework import serializers
from .models import Employee
from django.utils import timezone


class UserSerializer(serializers.ModelSerializer):
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
    password = serializers.CharField(style={'input_type': 'password'})

    # date_joined = serializers.DateTimeField(default=timezone.now, format='%d %B %Y %H:%M')

    groups = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name',
    )

    def validate(self, data):
        """
            Check that email ends with @gmail.com
        """
        if not data['email'].endswith('@gmail.com'):
            raise serializers.ValidationError(
                "Wrong email format: Please make sure to write @gmail.com")
        return data

    def create(self, validated_data):
        return Employee.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """
            Update an employee: password and email.
        """
        instance.set_password(validated_data['password'])
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.role = validated_data.get('role', instance.role)
        instance.is_superuser = validated_data.get('is_superuser', instance.is_superuser)

        instance.save()
        return instance
