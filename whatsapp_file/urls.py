from django.urls import path
from . import views

urlpatterns = [
    path('hello-world/', views.hello_world, name='hello_world'),
    path('create/', views.user_create, name='user-create'),
    # path('todos/', views.todo_list, name='todo-list'),
    # path('todos/<int:pk>/', views.todo_detail, name='todo-detail'),

    path('todos/', views.TodoListCreateView.as_view(), name='todo-list-create'),
    path('todos/<int:pk>/', views.TodoRetrieveUpdateDestroyView.as_view(), name='todo-detail'),
]