from django.urls import path
from .views import *

urlpatterns = [
    path('hello_world/', hello_world),
    path('user_create/', user_create,name='user_create'),
    path("disp_tbl/",disp_tbl,name="disp_tbl"),
    path('register/',register,name='register'),
    path('login/',login,name='login')
]