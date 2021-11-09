from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.decorators import authentication_classes
from rest_framework.decorators import permission_classes
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Message, Restaurant, Supplier, UserProfile, Product
from .serializers import SupplierSerializer, RestaurantSerializer


# API Views.
# Token Authentication is set by default so all views need Token to respond
# When serializing many=true is run when serializing lists, while many=false when serializing instance

@api_view(['GET'])
def getMessages(request):
    testMessages = {"key1": "abc",
                    "key2": "xyz",
                    "key3": "lmn"}

    print(request.user)

    return Response(testMessages)


@api_view(['GET'])
def getSupplierScreenInfo(request):
    currentUser = request.user

    # Get restaurant data
    restaurant = UserProfile.objects.get(user=currentUser).restaurant
    restaurantSerializer = RestaurantSerializer(restaurant)
    # get supplier data
    suppliers = Supplier.objects.filter(restaurant_id=restaurant)
    supplierSerializer = SupplierSerializer(suppliers, many=True)

    # Get last messages for all suppliers of the user
    lastMessages = {}

    for supplier in suppliers:
        chatGroup = str(restaurant.id) + '_' + str(supplier.id)
        try:
            lastMessage = Message.objects.order_by('-timestamp').filter(
                chatgroup=chatGroup)[0].content
        except:
            lastMessage = ''
        lastMessages[chatGroup] = lastMessage

    print(lastMessages)

    return Response([restaurantSerializer.data, supplierSerializer.data, request.user.username, lastMessages])
