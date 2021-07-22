from django.contrib import admin
from django.urls import path
from django import urls
from django.urls.conf import include
from .import views
from .views import LoginView,RegistrationView,LogoutView,VerificationView

urlpatterns = [
   path('register',RegistrationView.as_view(), name='register'),
   path('login',LoginView.as_view(), name='login'),
   path('logout',LogoutView.as_view(), name='logout'),
   path('activate/<uidb64>/<token>',VerificationView.as_view(),name='activate'),
]
