from django.shortcuts import render,get_object_or_404
from .serializers import *
from .models import *
from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail



class Registration_usersView(APIView):
    def post(self, request):
        serializer = Approval_user_Serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self,request):
        users=Approval_user.objects.all()
        serializer=update_user_serealizer(users,many=True)
        return Response(serializer.data)

class users_updateview(APIView):
    def get(self, request, *args, **kwargs):
        user = get_object_or_404(Approval_user, pk=kwargs['pk'])
        serializer = update_user_serealizer(user)
        return JsonResponse(serializer.data)

    def put(self, request, *args, **kwargs):
        user = get_object_or_404(Approval_user, pk=kwargs['pk'])
        data = JSONParser().parse(request)
        serializer = update_user_serealizer(user, data=data)
        if serializer.is_valid():
            serializer.save()

            name=serializer.validated_data['name']
            status=serializer.validated_data['status']
            email=serializer.validated_data['email']

            if status==True:
                message="Approved"
            elif status==False:
                message="Rejected"

            try:
                send_mail(
                    'Approval Request',
                    f'Dear {name}, Your Approval Request has been {message}',
                    'ajaynowdasari4@gmail.com',
                    [email],
                    fail_silently=False,
                )
            except Exception as e:
                return Response(f'An error occurred: {str(e)}', status=500)
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        user = get_object_or_404(Approval_user, pk=kwargs['pk'])
        name=user.name
        try:
            send_mail(
                'Approval Request',
                f'Dear {name}, Your Approval Request has been Removed from Database please request Again by Registering as user Again,Thank you.' ,
                'sujanpanda049@gmail.com',
                [user.email],
                fail_silently=False,
            )
        except Exception as e:
                return Response(f'An error occurred: {str(e)}', status=500)
        user.delete()
        return JsonResponse({}, status=status.HTTP_204_NO_CONTENT)

class user_Login_view(APIView):
    def post(self, request):
        serializer=user_LoginSerializer(data=request.data)
        if serializer.is_valid():

            user=serializer.validated_data['user']
            return Response({
                "id":user.id
                },status=status.HTTP_200_OK)
        
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class Admin_Login_view(APIView):
    def post(self, request):
        serializer=Admin_Login_Serializer(data=request.data)
        if serializer.is_valid():
            user=serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)
            refresh['username'] = user.username 
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)

            return Response({
                "access_token": access_token,
                "refresh_token": refresh_token,
                },status=status.HTTP_200_OK)

        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
class Cart_view(APIView):
    def post(self, request):
        serializer= Cart_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response({'error':"something went wrong"},status=status.HTTP_400_BAD_REQUEST)

class Cart_items(APIView):
    def get(self, request, *args, **kwargs):
        user = Approval_user.objects.get(id=kwargs['id'])
        cart_items=productsCart.objects.filter(Approval_user=user)
        serializer = Cart_serializer(cart_items,many=True)
        return JsonResponse(serializer.data,safe=False)
    
    def put(self, request, *args, **kwargs):
        item = productsCart.objects.get(id=kwargs['id'])
        print(item,"ghdjah")
        data = JSONParser().parse(request)
        serializer = Cart_serializer(item, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse({'error':"Unable to update Cart item Quantity"}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        user = productsCart.objects.get(id=kwargs['id'])
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)