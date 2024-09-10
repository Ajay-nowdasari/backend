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

