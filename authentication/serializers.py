# authentication/serializers.py
from rest_framework import serializers
from .models import Employee
from django.utils import timezone


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={'input_type': 'password'})
    # date_joined = serializers.DateTimeField(default=timezone.now, format='%d %B %Y %H:%M')

    class Meta(object):
        model = Employee
        fields = ['email', 'password', 'first_name', 'last_name', 'role', 'is_superuser', 'date_joined']
        extra_kwargs = {
            'password': {'write_only': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
            'date_joined': {'default': timezone.now, 'format': '%d %B %Y %H:%M'}
        }

    def create(self, validated_data):
        user = Employee.objects.create_user(
            email=validated_data["email"],
            password=validated_data["password"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
        )
        return user
