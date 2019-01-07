from django.shortcuts import render, HttpResponse, redirect
from django.views.generic.base import View
import requests
import json
from django.contrib.auth.hashers import make_password
from django.db.models import Q
from robot.models import Chat, Users
from robot.forms import LoginForm, RegisterForm, registerForm
from django.contrib.auth import login, logout
# 验证码需要导入的模块
from captcha.models import CaptchaStore
from captcha.helpers import captcha_image_url

# 创建验证码
def captcha():
    # 验证码，第一次请求
    hashkey = CaptchaStore.generate_key()
    image_url = captcha_image_url(hashkey)
    captcha = {'hashkey': hashkey, 'image_url': image_url}
    return captcha
 
# 验证验证码
def jarge_captcha(captchaStr, captchaHashkey):
    if captchaStr and captchaHashkey:
        try:
            # 获取根据hashkey获取数据库中的response值
            get_captcha = CaptchaStore.objects.get(hashkey=captchaHashkey) 
            # 如果验证码匹配
            if get_captcha.response == captchaStr.lower():  
                return True
        except:
            return False
    else:
        return False

def refresh_captcha(request):
    return HttpResponse(json.dumps(captcha()), content_type='application/json')


class RegisterView(View):
    def get(self, request):
        captcha = captcha()
        register_form = RegisterForm()
        return render(request, "register.html", {'register_form': register_form, 'captcha': captcha})

    def post(self, request):
        captcha = captcha()
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            data = register_form.cleaned_data
            captchaHashkey = request.POST.get('hashkey', '') # 获取前端的hashkey值
            if jarge_captcha(data['captcha'], captchaHashkey):
                register_form.cleaned_data['password'] = make_password(register_form.cleaned_data['password'])
                Users.objects.create(**register_form.cleaned_data)
                # user_profile.is_active = False
                # send_email_register(email, 'register')
                return render(request, 'login.html', {'msg': "注册成功,请登录..."})
            else:
                return render(request, 'register.html', {'msg': "验证码错误"})
        else:
            return render(request, 'register.html', {'captcha': captcha, 'register_form': register_form})
            
