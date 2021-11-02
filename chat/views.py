from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.decorators import authentication_classes
from rest_framework.decorators import permission_classes
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Message


# Normal Views

def index(request):
    return render(request, 'chat/index.html')


def room(request, room_name):
    return render(request, 'chat/room.html', {
        'room_name': room_name
    })


# API Views

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getMessages(request):
    testMessages = {"key1": "abc",
                    "key2": "xyz",
                    "key3": "lmn"}

    return Response(testMessages)


# @authentication_classes([SessionAuthentication, BasicAuthentication])
# @permission_classes([IsAuthenticated])
