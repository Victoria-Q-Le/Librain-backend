from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Book
from .serializers import BookSerializer
from .books import books


@api_view(['GET'])
def getRoutes(request):
    routes = [
        '/api/books',
        '/api/books/create',

        '/api/books/upload',

        '/api/books/<id>/reviews',

        '/api/books/top/',
        '/api/books/<id>/',

        '/api/books/delete/<id>/',
        '/api/books/<update>/<id>',
    ]
    return Response(routes)

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
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        token['message'] = 'Hello World!'

        return token

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
