from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User

class Approval_user_Serializer(serializers.ModelSerializer):
    confirm_password=serializers.CharField(write_only=True)

    class Meta:
        model = Approval_user
        fields = ['id','name', 'phone','email','password','confirm_password',"status" ]

    def validate(self, attrs):
       
        name=attrs['name']
        if Approval_user.objects.filter(name=name).exists():
            raise serializers.ValidationError({"name_error": "A user with this username already exists."})
        
        email=attrs['email']
        if Approval_user.objects.filter(email=email).exists():
            raise serializers.ValidationError({"email_error": "A user with this email already exists."})
        
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"password_error": "Passwords do not match."})
        return attrs


    def create(self, validated_data):
        user = Approval_user.objects.create(
            name=validated_data['name'],
            phone=validated_data['phone'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user
    
class update_user_serealizer(serializers.ModelSerializer):
    class Meta:
        model=Approval_user
        fields="__all__"


class user_LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        email = data.get('email').lower().strip()
        password = data.get('password')
        print(email,"email",password,"password")
        if email and password:
            user = Approval_user.objects.get(email=email)
            print(f"User found: {user}")
            if user.password==password:
                data["user"]=user
            else:
                raise serializers.ValidationError("wrong password.")
        else:
            raise serializers.ValidationError("Must include 'email' and 'password'.")

        return data

class Admin_Login_Serializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        email = data.get('email').lower().strip()
        password = data.get('password')

        if email and password:
            user = User.objects.get(email=email)
            print(f"User found: {user}")
            if user.check_password(password):
                data['user']=user
            else:
                raise serializers.ValidationError("wrong password.")
        else:
            raise serializers.ValidationError("Must include 'email' and 'password'.")

        return data
    
    class Cart_serializer(serializers.ModelSerializer):
        class Meta:
            model=productsCart
            fields="__all__"