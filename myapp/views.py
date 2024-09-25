from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import *
from rest_framework import status
from .models import *
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication

@api_view(['GET'])
def hello_world(request):
    return Response({'context': 'pani - ledu!'})

@api_view(['POST'])
def user_create(request):
    serializer = UserSerializer(data = request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def disp_tbl(request):
    members = user.objects.all()  # Fetch all users
    serializer = UserSerializer(members, many=True)  # Serialize the queryset
    return Response(serializer.data, status=status.HTTP_200_OK)  # Return serialized data with HTTP 200 status


@api_view(['POST'])
def register(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def login(request):
    members = Register.objects.all()
    serializer = RegisterSerializer(members,many=True)
    return Response(serializer.data,status= status.HTTP_200_OK) 


class AdminLoginView(APIView):
    def post(self, request):
        serializer = AdminLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']

            print(user.username,user.password)
           
            refresh = RefreshToken.for_user(user)
            refresh['username'] = user.username 
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)

            return Response({
                "access_token": access_token,
                "refresh_token": refresh_token
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class StudentretriveView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    queryset = User.objects.all()
    serializer_class = UserSerializer


@api_view(['POST'])
def product_users(request):
    Serializer=ProductUserSerializer(data=request.data)
    if Serializer.is_valid():
        Serializer.save()

        username=Serializer.validated_data['username']
        email=Serializer.validated_data['email']
        password=Serializer.validated_data['password']

        user=User(username=username,email=email)
        user.set_password(password)
        user.save()

        return Response(Serializer.data,status=status.HTTP_201_CREATED)
    return Response(Serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def product_admins(request):
    Serializer=ProductAdminSerializer(data=request.data)
    if Serializer.is_valid():
        Serializer.save()

        return Response(Serializer.data,status=status.HTTP_201_CREATED)
    return Response(Serializer.errors, status=status.HTTP_400_BAD_REQUEST)


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import send_mail
from .serializers import ProductLoginSerializer

class ProductLoginView(APIView):
    def post(self, request):
        serializer = ProductLoginSerializer(data=request.data)
        if serializer.is_valid():
            admin = serializer.validated_data.get('admin')  
            user = serializer.validated_data.get('user') 
            
            if admin:
                refresh = RefreshToken.for_user(admin)
                refresh['username'] = admin.username
                access_token = str(refresh.access_token)
                refresh_token = str(refresh)
                username = admin.username
                usertype = "admin"
            elif user:
                refresh = RefreshToken.for_user(user)
                refresh['username'] = user.username
                access_token = str(refresh.access_token)
                refresh_token = str(refresh)
                username = user.username
                usertype = "user"
            else:
                return Response({"error": "No valid user found"}, status=status.HTTP_400_BAD_REQUEST)

            otp_instance = OTP(user=admin if admin else user)
            otp_instance.save()

            try:
                send_mail(
                    'Your OTP Code',
                    f'Your OTP code is {otp_instance.otp}',
                    'ajaynowdasari4@gmail.com',
                    [admin.email if admin else user.email],
                    fail_silently=False,
                )
            except Exception as e:
                return Response(f'An error occurred: {str(e)}', status=500)

            return Response({
                "username": username,
                "usertype": usertype,
                "access_token": access_token,
                "refresh_token": refresh_token
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyOTPView(APIView):
    def post(self, request):
        try:
            user = User.objects.get(username=request.data.get('username'))
            otp = request.data.get('otp')
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        try:
             OTP.objects.get(user=user, otp=otp)
        except OTP.DoesNotExist:
            return Response({'error': 'Indvalid OTP'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'success': 'OTP verified'}, status=status.HTTP_200_OK)


class Products_view(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
