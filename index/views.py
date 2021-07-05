from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from user_auth.models import UserInfo as User
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.views.decorators import csrf


@login_required
def homepage(request):
    return render(request, "index/search.html")


@login_required
def search(request):
    url = "https://item.taobao.com/item.htm?ft=t&id=557459153638&ali_trackid=2:mm_26632614_0_0:1625294291_214_1693929474&union_lens=recoveryid:1625294291_214_1693929474&spm=a21bo.7925890.192091.3&bxsign=tbkYsOuoO1yaNdgwU6fgE1U+XxyC8ixcd+aHg2BEncYq4nxi0ih5FXwuzu4Hv5gALygW7fJAZ6zj7eowsN4GjWbSztHvIcEzH4IS9F2a1ZmyNo="
    return HttpResponse("1")

# Create your views here.
