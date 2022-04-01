from django.urls import path
from . import views



urlpatterns = [
    path('',views.getRoutes, name = 'routes'),
    path('books/', views.getBooks, name = 'books'),
    path('books/<int:pk>/', views.getBook, name = 'book'),

    path('users/login/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'), #remove the api from this url because our base url already include /api/.Once log in this route will provide 2 tokens: access token and refresh token, the access token will be used to send to protected routes, and because I want to use the customize token so I changed the view from 'TokenObtainPairView' to 'MyTokenObtainPairView'
]
