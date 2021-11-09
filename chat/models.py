from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Restaurant(models.Model):

    name = models.CharField(max_length=100)
    legal_name = models.CharField(max_length=200)
    tax_id = models.IntegerField()

    def __str__(self):
        return self.name


class Supplier(models.Model):

    name = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    tax_id = models.IntegerField()
    phone = models.IntegerField()
    address = models.CharField(max_length=500)
    contact = models.CharField(max_length=500)
    restaurant_id = models.ManyToManyField(Restaurant)


class UserProfile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(
        Restaurant, on_delete=models.CASCADE, null=True, blank=True)
    supplier = models.ForeignKey(
        Supplier, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.user.username


class Product(models.Model):

    name = models.CharField(max_length=100)
    restaurant = models.CharField(max_length=100)
    sku = models.CharField(max_length=100)
    supplier_id = models.ForeignKey(Supplier, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Message(models.Model):

    content = models.TextField()
    # TODO: Sender needs to be linked to user model
    # sender = models.ForeignKey(User, on_delete=models.CASCADE)
    sender = models.CharField(max_length=100)
    chatgroup = models.CharField(max_length=100, editable=False)
    timestamp = models.DateTimeField(auto_now_add=True)
