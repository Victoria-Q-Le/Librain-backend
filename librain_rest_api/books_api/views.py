from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from .models import Book
from django.contrib.auth.models import User
from .serializers import BookSerializer, UserSerializer, UserSerializerWithToken
from .books import books
from django.contrib.auth.hashers import make_password
from rest_framework import status


#############the Books views###################
@api_view(['GET'])
def getBooks(request):
    books = Book.objects.all()
    serializer = BookSerializer(books, many = True)
    return Response(serializer.data)


@api_view(['GET'])
def getBook(request,pk):
    book = Book.objects.get(id = pk)
    serializer = BookSerializer(book, many = False)
    return Response(serializer.data)


# I want to further customize my tokens so it will give back more information then just the expiration and user id, thus avoiding making additional api call for other information, read Customizing Token Claims for more information.
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        serializer = UserSerializerWithToken(self.user).data
        for k,v in serializer.items():
            data[k] = v
        return data

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

@api_view(['POST'])
def registerUser(request):
    data = request.data
    user = User.objects.create(
        first_name = data['name'],
        username = data['email'],
        email  = data['email'],
        password = make_password(data['password'])
    )
    serializer = UserSerializerWithToken(user, many=False)
    return Response(serializer.data)

###########The Users views#################
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUserProfile(request):
    user = request.user
    serializer = UserSerializer(user, many = False)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAdminUser])
def getUsers(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many = True)
    return Response(serializer.data)
