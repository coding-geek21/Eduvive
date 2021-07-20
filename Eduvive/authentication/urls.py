from django.contrib import admin
from django.urls import path
from django import urls
from django.urls.conf import include
from .import views

urlpatterns = [
   path('login/',views.login,name="login"),
]
