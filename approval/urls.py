from django.urls import path
from .views import *

urlpatterns = [
      path('Register-user/',Registration_usersView.as_view(), name='Register-user'),
      path('Register-user/<int:pk>/',users_updateview.as_view(), name='edit_user'),

      path('user-login/',user_Login_view.as_view(),name="user-login"),
      path('admin-login/',Admin_Login_view.as_view(),name="admin-login")

]