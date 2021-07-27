from django.contrib import admin
from django.urls import path
from django import urls
from django.urls.conf import include
from .views import Reset_Newpassword_form,LoginView,RegistrationView,LogoutView,VerificationView,Forget_PasswordView, Password_reset_form
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from authentication import views


urlpatterns = [
   path('register',RegistrationView.as_view(), name='register'),
   path('login',LoginView.as_view(), name='login'),
   path('logout',LogoutView.as_view(), name='logout'),
   path('activate/<uidb64>/<token>',VerificationView.as_view(),name='activate'),
   path('forgot-password', Forget_PasswordView.as_view(),name='forgot-password'),
   path('reset-password',Reset_Newpassword_form.as_view(),name='reset-password'),
   path("reset-password/<uidb64>/<token>", Password_reset_form.as_view() , name='reset-password'),
   path('set-newpassword/',login_required(views.ChangePasswordView.as_view(),login_url='login'), name='set-newpassword'),
]
