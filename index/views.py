import time

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from user_auth.models import UserInfo as User
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.views.decorators import csrf
from django.urls import reverse


@login_required
def homepage(request):
    return render(request, "index/search.html")


def jump_homepage(request):
    return HttpResponseRedirect(reverse("index_homepage"))


@login_required
def search(request):
    print(request)
    url = request.POST.get('url')
    time.sleep(1)
    return JsonResponse({"success": True, "message": url})

# Create your views here.

