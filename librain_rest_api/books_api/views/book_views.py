from django.shortcuts import render
from rest_framework.response import Response
from books_api.models import Book
from books_api.serializers import BookSerializer
from rest_framework.decorators import api_view

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
