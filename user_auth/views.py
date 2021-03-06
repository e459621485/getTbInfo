from django.shortcuts import render
from django.contrib import auth
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from user_auth.valid_code import ValidCodeImg
from django.views.decorators import csrf


def reg(request):
    context = {}
    return render(request, "user_auth/reg.html", context)


def login(request):
    context = {}
    return render(request, "user_auth/login.html", context)



def auth_ajax(request):
    res = {}
    if request.method == "GET":
        return HttpResponseRedirect(reverse('auth_login'))
    user = request.POST['user']
    pwd = request.POST['password']
    captcha = request.POST["captcha"]
    if captcha.upper() != request.session.get('valid_code').upper():
        res['success'] = False
        res["message"] = "验证码错误"
        return JsonResponse(res)
    if not User.objects.filter(username=user):
        res['success'] = False
        res["message"] = "用户不存在"
        return JsonResponse(res)
    user_obj = auth.authenticate(username=user, password=pwd)
    if not user_obj:
        res['success'] = False
        res["message"] = "密码错误"
        return JsonResponse(res)
    else:
        auth.login(request, user_obj)
        res['success'] = True
        res["message"] = "登录成功，点击确定跳转主页"
        return JsonResponse(res)


def add_ajax(request):
    res = {}
    if request.POST:
        user = request.POST['user']
        pwd = request.POST['password']
        confirm_pwd = request.POST['confirm_password']
        captcha = request.POST["captcha"]
        if captcha.upper() != request.session.get('valid_code').upper():
            res['success'] = False
            res["message"] = "验证码错误"
            return JsonResponse(res)
        if confirm_pwd != pwd:
            res['success'] = False
            res["message"] = "两次输入的密码不一致"
            return JsonResponse(res)
        if User.objects.filter(username=user):
            res["success"] = False
            res["message"] = '用户名重复，请重新注册'
            return JsonResponse(res)
        User.objects.create_user(username=user, password=pwd)
        user_obj = auth.authenticate(username=user, password=pwd)
        auth.login(request, user_obj)
        res["success"] = True
        res["message"] = '注册成功，点击确定跳转主页'
        return JsonResponse(res)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse("auth_login"))


def get_valid_code_img(request):
    obj = ValidCodeImg()
    img_data, valid_code = obj.getValidCodeImg()
    request.session['valid_code'] = valid_code
    return HttpResponse(img_data)

# Create your views here.
