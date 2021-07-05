from django.shortcuts import render
from django.contrib import auth
from user_auth.models import UserInfo as User
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.views.decorators import csrf


def reg(request):
    context = {
        "title": "注册",
        "action": reverse('auth_add_user'),
        "sub_text": "注册",
        "jump": reverse('auth_login'),
        "jump_text": "去登陆",
        "homepage": reverse('index_homepage'),
    }
    return render(request, "user_auth/user_auth.html", context)


def login(request):
    context = {
        "title": "登陆",
        "action": reverse('auth_auth_user'),
        "sub_text": "登陆",
        "jump": reverse('auth_reg'),
        "jump_text": "去注册",
        "homepage": reverse('index_homepage'),
    }
    return render(request, "user_auth/user_auth.html", context)


def add_user(request):
    if request.POST:
        try:
            user = request.POST['user']
            pwd = request.POST['password']
            if User.objects.filter(username=user):
                return HttpResponse("用户名重复，请重新注册")
            User.objects.create_user(username=user, password=pwd)
            user_obj = auth.authenticate(username=user, password=pwd)
            auth.login(request, user_obj)
            return HttpResponseRedirect(reverse('index_homepage'))
        except:
            return HttpResponse("注册失败")


def auth_user(request):
    if request.method == "GET":
        return HttpResponseRedirect(reverse('auth_login'))
    user = request.POST.get("user")
    pwd = request.POST.get("password")
    user_obj = auth.authenticate(username=user, password=pwd)
    if not user_obj:
        return HttpResponseRedirect(reverse('auth_login'))
    else:
        auth.login(request, user_obj)
        return HttpResponseRedirect(reverse('index_homepage'))


def auth_ajax(request):
    res = {}
    if request.method == "GET":
        return HttpResponseRedirect(reverse('auth_login'))
    user = request.POST.get("user")
    pwd = request.POST.get("password")
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

# Create your views here.