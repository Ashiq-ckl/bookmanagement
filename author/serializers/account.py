from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from ..validators import validate_possible_number

class SigninSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    def validate(self, attrs):
        response = {}
        user = authenticate(username=attrs['username'],password=attrs['password'])
        if user and not user.is_active:
            response['message'] = 'Your account has blocked'
        elif user is None:
            response['message'] = 'Invalid username or password.'
        if response:
            raise serializers.ValidationError(response)
        return super().validate(attrs)