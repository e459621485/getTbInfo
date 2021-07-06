import time
import requests
import re
import json
import urllib.parse

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from user_auth.models import UserInfo as User
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.views.decorators import csrf
from django.urls import reverse
from index.models import tbInfo


@login_required
def homepage(request):
    return render(request, "index/search.html")


def jump_homepage(request):
    return HttpResponseRedirect(reverse("index_homepage"))


@login_required
def search(request):
    requests.packages.urllib3.disable_warnings()
    req_session = requests.Session()
    url = request.POST.get('url')
    headers = {
        'referer': 'https://www.taobao.com/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }
    response = req_session.get(url, headers=headers, verify=False, timeout=5)
    try:
        if "taobao" in url:
            title = re.search(r'.*tb-main-title.*\s(.*)', response.text).group(1).strip()
            price = re.search(r'tb-rmb-num">(.*?)<', response.text).group(1)
            seller = re.search(r'.*tb-seller-name.*\s(.*)', response.text).group(1).strip()
            img = re.search(r'.*J_ImgBooth"\s.*src="(.*?)"', response.text).group(1)
            res = {"success": True, "message": '获取淘宝数据成功'}
        elif "tmall" in url:
            goods_match = re.search(r'"itemDO":{(.*?)}', response.text)
            data = json.loads('{' + goods_match.group(1) + '}')
            title = data['title']
            price = data['reservePrice']
            seller = urllib.parse.unquote(data['sellerNickName'])
            img = re.search(r'.*J_ImgBooth"\s.*src="(.*?)"', response.text).group(1)
            res = {"success": True, "message": '获取天猫数据成功'}
        else:
            res = {"success": False, "message": '请输入淘宝或天猫的url'}
            return JsonResponse(res)
        tb_info = tbInfo(
            title=title,
            price=price,
            seller=seller,
            img=img,
        )
        tb_info.save()
    except Exception as e:
        res = {"success": False, "message": '获取数据失败啦，换个url试试吧'}
    return JsonResponse(res)


def result(request):
    context = {
        'result': tbInfo.objects.values().last(),
    }

    return render(request, "index/result.html", context)


def result_id(request, id):
    context = {
        'result': tbInfo.objects.values().filter(id=id),
    }

    return render(request, "index/result.html", context)

# Create your views here.

