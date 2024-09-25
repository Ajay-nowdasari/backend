from django.db import models
from myapp.models import Product
from django.contrib.auth.models import User

class Approval_user(models.Model):
    name=models.CharField(max_length=50)
    phone=models.IntegerField()
    email=models.EmailField()
    password=models.CharField(max_length=60)
    status=models.BooleanField(max_length=10,null=True)
    def __str__(self):
        return f"{self.name}"


class productsCart(models.Model):
    Approval_user = models.ForeignKey(Approval_user, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart_quantity=models.IntegerField()
    def __str__(self):
        return f"{self.Approval_user.name} {self.product.product} {self.product.quality}"