from django.urls import path
from books_api.views import book_views as views



urlpatterns = [
    path('', views.getBooks, name = 'books'),
    path('<int:pk>/', views.getBook, name = 'book'),

]
