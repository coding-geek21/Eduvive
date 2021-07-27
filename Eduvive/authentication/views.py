from os import link
import re
from django.shortcuts import redirect, render
from django.views import View
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import EmailMessage
from django.core.mail import send_mail
from django.urls import reverse
from django.utils.encoding import force_bytes, force_text , DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from .utils import token_generator
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.hashers import check_password
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

# Create your views here.


class RegistrationView(View):
    def get(self, request):
        return render(request,'authentication/register.html')

    def post(self, request):
        #create a user account

        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():
                    if len(password)<6:
                        messages.error(request,'Password is too short')
                        return render(request, 'authentication/register.html')
                    user = User.objects.create_user(username=username, email=email)
                    user.set_password(password)
                    user.is_active = False
                    user.save()

                    uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
                    domain = get_current_site(request).domain
                    link = reverse('activate',kwargs={'uidb64':uidb64,'token': token_generator.make_token(user)})

                    email_subject = 'Activate your account'
                    activate_url = 'http://'+domain+link
                    email_body = 'Hi, '+ user.username + \
                        ' Please use this link to verify your account\n'+ activate_url
                    email = EmailMessage(
                    email_subject,
                    email_body,
                    'from@example.com',
                    [email],
                    )
                    email.send(fail_silently=False)
                    messages.success(request,'Account successfully created! Check your Email for Account Activation')
                    return render(request, 'authentication/register.html' )
                    
            return render(request,'authentication/register.html')
        else : 
            return render(request,'authentication/register.html')

class VerificationView(View):
    def get(self, request, uidb64, token):

        try:
            id = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=id)

            if not token_generator.check_token(user,token):
                return redirect('login'+'?message='+'User already activated')

            if user.is_active:
                return redirect('login')
            user.is_active = True
            user.save()

            messages.success(request, 'Account activated successfully')
            return redirect('login')
        except Exception as ex:
            pass

        
        return redirect('login')

class LoginView(View):
    def get(self,request):
        return render(request,'authentication/login.html')
    
    def post(self,request):
        username = request.POST['username']
        password = request.POST['password']

        if username and password:

            user = auth.authenticate(username=username , password=password)

            if user:
                if user.is_active:
                    auth.login(request, user)
                    messages.success(request, 'Welcome, ' + 
                                    user.username + ' you are now logged in')
                    return redirect('dashboard')

                messages.error(
                    request, 'Account is not active, please check your email')
                return render(request,'authentication/login.html')
            messages.error(
                request, 'Invalid credentials, try again')
            return render(request,'authentication/login.html')
        messages.error(
            request, 'Please fill all the fields')
        return render(request,'authentication/login.html')


class LogoutView(View):
    def get(self, request):
        user_crr = request.user
        auth.logout(request)
        messages.success(request, f'{user_crr} you have been logged out')
        return redirect('login')
