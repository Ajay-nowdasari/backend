from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = user
        fields = ['first_name','last_name','email','password']

class RegisterSerializer(serializers.ModelSerializer):
    # confirm_password = serializers.CharField(max_length =16)
    class Meta:
        model = Register
        fields = ['first_name','last_name','email','password']

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

class ProductUserSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = ProductUser
        fields = ['username', 'email', 'password', 'confirm_password']

    def validate(self, attrs):
        
        if ProductUser.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError({"email_error": "A user with this email already exists."})

        
        if ProductUser.objects.filter(username=attrs['username']).exists():
            raise serializers.ValidationError({"username_error": "A user with this username already exists."})

    
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"password_error": "Passwords does not match."})

        return attrs
    
    

    def create(self, validated_data):
        user = ProductUser(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user
    
class ProductAdminSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'confirm_password']

    def validate(self, attrs):
        
        if ProductUser.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError({"email_error":["A user with this email already exists."]})

        
        if ProductUser.objects.filter(username=attrs['username']).exists():
            raise serializers.ValidationError({"username_error": "A user with this username already exists."})

    
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"password_error": "Passwords does not match."})

        return attrs
    
    def create(self, validated_data):
        user = User.objects.create_superuser(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        
        return user

class ProductLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        email = data.get('email').lower().strip()
        password = data.get('password')

        if email and password:
            user = User.objects.get(email=email)
            print(f"User found: {user}")
            if user.check_password(password):
                if user.is_superuser:
                    data['admin'] = user
                    print(f"Admin user: {data['admin']}")
                else:
                    data['user'] = user
                    print(f"Regular user: {data['user']}")
            else:
                raise serializers.ValidationError("wrong password.")
        else:
            raise serializers.ValidationError("Must include 'email' and 'password'.")

        return data



class OTPSerializer(serializers.ModelSerializer):
    class Meta:
        model = OTP
        fields = ['user', 'otp']

    def create(self, validated_data):
        otp_instance = OTP.objects.create(**validated_data)
        return otp_instance

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'