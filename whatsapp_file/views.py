from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from rest_framework import generics
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import User,TodoItem
from .serializers import UserSerializer,TodoItemSerializer

@api_view(['GET'])
def hello_world(request):
    return Response({'message': 'Hii this is krify'})

@api_view(['POST'])
def user_create(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
def todo_list(request):
    if request.method == 'GET':
        todos = TodoItem.objects.all()
        serializer = TodoItemSerializer(todos, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = TodoItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def todo_detail(request, pk):
    todo = get_object_or_404(TodoItem, pk=pk)
    
    if request.method == 'GET':
        serializer = TodoItemSerializer(todo)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = TodoItemSerializer(todo, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    elif request.method == 'PATCH':
        serializer = TodoItemSerializer(todo, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        todo.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    


class TodoListCreateView(generics.ListCreateAPIView):
    queryset = TodoItem.objects.all()
    serializer_class = TodoItemSerializer

class TodoRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = TodoItem.objects.all()
    serializer_class = TodoItemSerializer



# views.py
from django.views import View
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import TodoItem
from .serializers import TodoItemSerializer
from rest_framework.parsers import JSONParser
from rest_framework import status

class TodoItemView(View):
    def get(self, request, *args, **kwargs):
        todos = TodoItem.objects.all()
        serializer = TodoItemSerializer(todos, many=True)
        return JsonResponse(serializer.data, safe=False)

    def post(self, request, *args, **kwargs):
        data = JSONParser().parse(request)
        serializer = TodoItemSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TodoItemDetailView(View):
    def get(self, request, *args, **kwargs):
        todo = get_object_or_404(TodoItem, pk=kwargs['pk'])
        serializer = TodoItemSerializer(todo)
        return JsonResponse(serializer.data)

    def put(self, request, *args, **kwargs):
        todo = get_object_or_404(TodoItem, pk=kwargs['pk'])
        data = JSONParser().parse(request)
        serializer = TodoItemSerializer(todo, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        todo = get_object_or_404(TodoItem, pk=kwargs['pk'])
        todo.delete()
        return JsonResponse({}, status=status.HTTP_204_NO_CONTENT)
