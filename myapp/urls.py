from django.urls import path
from .views import *

urlpatterns = [
    path('hello_world/', hello_world),
    path('user_create/', user_create,name='user_create'),
    path('disp_tbl/',disp_tbl,name="disp_tbl"),
    path('register/',register,name='register'),
    path('login/',login,name='login'),
    path('adminlogin/',AdminLoginView.as_view(),name="adminlogin"),
    path('students/',StudentretriveView.as_view(),name="students"),
    
    path('Usercreation/',product_users,name='Usercreation'),
    path('Admincreation/',product_admins,name='Admincreation'),

    path('Productlogin/',ProductLoginView.as_view(),name="adminlogin"),
    path('verify-otp/', VerifyOTPView.as_view(), name='verify_otp'),

    path('Products/',Products_view.as_view(), name='product-list-create'),
    path('Products/<int:pk>/',ProductRetrieveUpdateDestroyView.as_view(), name='product-detail'),

]