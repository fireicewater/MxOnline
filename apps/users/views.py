from django.contrib.auth.backends import ModelBackend
from django.shortcuts import render
from django.contrib.auth import authenticate, login, hashers

from users.forms import LoginForm, RegisterForm,ForgetPwdForm,ModifyPwdForm
from users.models import UserProfile, EmailVerifyRecord
from django.db.models import Q
from django.views.generic.base import View
from utils.email_send import send_register_email


# Create your views here.
class CustomBackend (ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get (Q (username=username) | Q (email=username))
            if user.check_password (password):
                return user
        except Exception as e:
            return None


class LoginView (View):
    def get(self, request):
        return render (request, "login.html", {})

    def post(self, request):
        login_form = LoginForm (request.POST)
        if login_form.is_valid ():
            username = request.POST.get ("username", "")
            password = request.POST.get ("password", "")
            user = authenticate (username=username, password=password)
            if user is not None:
                if user.is_active:
                    login (request, user)
                    return render (request, "index.html", {})
                else:
                    return render (request, "login.html", {"msg": "用户未激活"})
            else:
                return render (request, "login.html", {"msg": "用户名密码错误"})
        else:
            return render (request, "login.html", {"login_form": login_form})


class RegisterView (View):
    def get(self, request):
        resiger_form = RegisterForm ()
        return render (request, "register.html", {'resiger_form': resiger_form})

    def post(self, request):
        resiger_form = RegisterForm (request.POST)
        if resiger_form.is_valid ():
            user_name = request.POST.get ("eamil", "")
            passoword = request.POST.get ("password", "")
            user_profile = UserProfile ()
            if UserProfile.objects.filter (email=user_name):
                return render (request, "register.html", {'resiger_form': resiger_form, 'msg': '用户名已注册'})
            user_profile.username = user_name
            user_profile.email = user_name
            user_profile.is_active = False
            user_profile.password = hashers.make_password (passoword)
            user_profile.save ()
            send_register_email (user_name)
            return render (request, "login.html")
        else:
            return render (request, "register.html", {'resiger_form': resiger_form})


class ActiveUserView (View):
    def get(self, request, active_code):
        record = EmailVerifyRecord.objects.get (code=active_code)
        if record:
            email = record.email
            user = UserProfile.objects.get (email=email)
            user.is_active = True
            user.save ()
            return render (request, "login.html")
        else:
            return render (request, "active_fail.html")


class ForgetPwdView(View):
    def get(self,request):
        forgetpwd_form=ForgetPwdForm()
        return render(request,"forgetpwd.html",{'forgetpwd_form':forgetpwd_form})

    def post(self,request):
        forgetpwd_form=ForgetPwdForm(request.POST)
        if forgetpwd_form.is_valid():
            email=request.POST.get("email","")
            send_register_email(email=email,type="forget")
            return render(request,"send_success.html")
        else:
            return render(request,"forgetpwd.html",{'forgetpwd_form':forgetpwd_form})

class ResetView (View):
    def get(self, request, active_code):
        record = EmailVerifyRecord.objects.get (code=active_code)
        if record:
            email = record.email
            return render (request, "password_reset.html",{'eamil':email})
        else:
            return render (request, "active_fail.html")


class ModifyView(View):
    def post(self,request):
        modify_form=ModifyPwdForm(request.POST)
        email=request.POST.get("email","")
        if modify_form.is_valid():
            passowrd=request.POST.get("passowrd","")
            passowrd2=request.POST.get("password2","")
            if passowrd!=passowrd2:
                return render(request,"password_reset.html",{"email":email,"msg":"密码不一致"})
            user=UserProfile.objects.get(email=email)
            user.password=hashers.make_password(passowrd)
            user.save()
            return render(request,"login.html")
        else:
            return render(request,"password_reset.html",{"email":email,"modify_form":modify_form})
