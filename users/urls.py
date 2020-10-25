"""Definiuje wzorce adresów URL dla aplikacji users."""

from django.urls import path, include
from . import views


app_name = 'users'
urlpatterns = [
    #Dołączanie domyślnych adresów URL uwierzytelniania
    path('', include('django.contrib.auth.urls')),
    #Stron rejestracji.
    path('register/', views.register, name='register'),
]