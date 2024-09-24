from django.contrib import admin
from django.urls import path, include
from app import views as v

urlpatterns = [
    path('home', v.homepage, name="homepage"),
    path('', v.landingPage, name="landingPage"),
    path('login', v.user_login, name="login"),
    path('register', v.register, name="register"),
    path('crypto-details/', v.crypto_details, name='crypto_details'),
    path('logout', v.user_logout, name="logout"),
]