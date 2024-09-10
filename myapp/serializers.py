from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name','last_name','email','password']

class RegisterSerializer(serializers.ModelSerializer):
    # confirm_password = serializers.CharField(max_length =16)
    class Meta:
        model = Register
        fields = ['first_name','last_name','email','password']

from django.contrib.auth.models import User
from rest_framework import serializers


class AdminLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if email and password:
            try:
                user = User.objects.get(email=email)
                
            except User.DoesNotExist:
                raise serializers.ValidationError("Unable to log in with provided credentials.")

            if user.check_password(password):
                if user.is_active and user.is_staff:
                    data['user'] = user
                else:
                    raise serializers.ValidationError("User is not active or not an admin.")
            else:
                raise serializers.ValidationError("Unable to log in with provided credentials.")
        else:
            raise serializers.ValidationError("Must include 'email' and 'password'.")

        return data