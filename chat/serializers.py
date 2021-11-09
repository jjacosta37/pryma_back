from rest_framework import serializers
from .models import Message, Restaurant, Supplier, UserProfile, Product


class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier()
        fields = ['id', 'name']


class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant()
        fields = ['id', 'name']
