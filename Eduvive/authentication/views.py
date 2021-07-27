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
        password1 = request.POST['password']
        password2 = request.POST['confirm-password']
        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():
                    if len(password1)<6:
                        messages.error(request,'Password is too short')
                        return render(request, 'authentication/register.html')
                    if(password1!=password2):
                        messages.error(request,"Two password doesn't match")
                        return render(request, 'authentication/register.html')

                    user = User.objects.create_user(username=username, email=email)
                    user.set_password(password1)
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

            messages.warning(request,"This Email already exists!")
            return render(request,'authentication/register.html')
        else : 
            messages.warning(request,"This username already exists!")
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


class ChangePasswordView(TemplateView):
    template_name='authentication/set-newpassword.html'
    def get(self,request):
        return render(request,'authentication/set-newpassword.html')
    
    def post(self,request):
        Current = request.POST['old-password']
        password_1= request.POST['new-password']
        password_2 = request.POST['confirm-password']
        if request.user.is_authenticated:
            user=request.user.username  
            pwd=request.user.password     
            u = User.objects.get(username=user) 
            if password_1!=password_2:
                messages.error(request,"Two passwords doesn't match")
                return render(request,'authentication/set-newpassword.html')
            if password_1.__len__()<9:
                messages.error(request,'New password must be at least 9 characters long')
                return render(request,'authentication/set-newpassword.html')
            try:
                user=User.objects.get(username=u)
            except ObjectDoesNotExist:
                messages.error(request,'User doesn not exist')
                return render(request,'authentication/set-newpassword.html')
            if user.check_password(Current)==False:
                messages.error(request,'Your current password is incorrect !')
                return render(request,'authentication/set-newpassword.html')
            else:
                user.set_password(password_1)
                user.save()
                auth.login(request, user)
                return redirect('EduviveData')

class Forget_PasswordView(View):
    def get(self,request):
        return render(request,'authentication/forgot-password.html')    
    
    def post(self,request):
        mail = request.POST['email'] 

        try:
            user=User.objects.get(email=mail)
            uidb64=urlsafe_base64_encode(force_bytes(user.pk))
            domain=get_current_site(request).domain
            link=reverse('reset-password',kwargs={'uidb64':uidb64,'token':token_generator.make_token(user)})

            reset_url = 'http://'+domain+link

            email_subject="Eduvive - Reset your Password!"
            email_body= "Hi  "+user.username+"  ,  Please use this link to Reset your Password\n" + reset_url
            email = EmailMessage(
                email_subject,
                email_body,
                'noreply@gmail.com',
                [mail],
            )
            
            email.send(fail_silently=False)
            messages.success(request,"We Have Sent you Mail!, Please Check It!")
            return render(request,'authentication/forgot-password.html')

        except User.DoesNotExist:
                messages.error(request,"User with this Email Address doesn't exist")
                return render(request,'authentication/forgot-password.html')

class Password_reset_form(View):
    def get(self, request, uidb64, token):
        try:
            id = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=id)

            if not token_generator.check_token(user,token):
                messages.success(request, 'Invalid Link !')
                return redirect('login')

            return redirect('reset-password')

        except Exception as ex:
            pass

        return redirect('reset-password')


class Reset_Newpassword_form(View):
    def get(self,request):
        return render(request,'authentication/reset-password.html')
    
    def post(self,request):
        new_pwd = request.POST['new-password-2']
        confirm_pwd = request.POST['confirm-password-2']
        user_email = request.POST['user_email']
        try:
            user=User.objects.get(email=user_email)

        except User.DoesNotExist:
                messages.error(request,"User with this Email Address doesn't exist")
                return render(request,'authentication/reset-password.html')
    
        if new_pwd!=confirm_pwd:
            messages.error(request,"Two passwords doesn't match")
            return render(request,'authentication/reset-password.html')
    
        if new_pwd.__len__()<9:
            messages.error(request,'New password must be at least 9 characters long')
            return render(request,'authentication/reset-password.html')
    
        else:
            user.set_password(confirm_pwd)  
            print(user.username)
            print(user.email)  
            user.save()
            auth.login(request, user)
            messages.success(request,'Your Password Reset Successfully Completed! Login using New Password!')
            return redirect('EduviveData')