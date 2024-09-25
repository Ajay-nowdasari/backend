from django.db import models

class user(models.Model):
    first_name = models.CharField(max_length=225)
    last_name = models.CharField(max_length=225)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=225)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    
class Register(models.Model):
    first_name = models.CharField(max_length=225)
    last_name = models.CharField(max_length=225)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=225)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'  
    
class ProductUser(models.Model):
    username=models.CharField(max_length=50)
    email = models.EmailField()
    password = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.username}"

class Product(models.Model):
    product=models.CharField(max_length=50)
    quality=models.IntegerField()
    quantity=models.IntegerField()
        
    def __str__(self):
        return f"{self.product}"


import random
from django.contrib.auth.models import User

class OTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6, blank=True) 

    def generate_otp(self):
        return str(random.randint(100000, 999999))

    def save(self):
        if not self.otp:
            self.otp = self.generate_otp()
        super().save()