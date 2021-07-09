import time
import requests
import re
import json
import urllib.parse
from datetime import datetime

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.views.decorators import csrf
from django.urls import reverse
from index.models import tbInfo
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


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
    response_text = response.text.replace('\n', '').replace('\r', '').replace(" ", '')
    try:
        if "taobao" in url:
            goods_match = re.search(r'item:{(.*?)},', response_text)
            response_text = goods_match.group(1)
            title = re.search(r"title:'(.*?)',", response_text).group(1).encode('latin-1').decode('unicode_escape')
            img = re.search(r"pic:'(.*?)',", response_text).group(1)
            price = re.search(r'tb-rmb-num">(.*?)<', response.text).group(1)
            seller = re.search(r"sellerNick:'(.*?)',", response_text).group(1)
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
            url=url,
            owner_id=request.user.id,
        )
        tb_info.save()
    except Exception as e:
        print(e)
        res = {"success": False, "message": '获取数据失败啦，换个url试试吧'}
    return JsonResponse(res)


@login_required
def result(request):
    result = tbInfo.objects.values().filter(owner=request.user.id).last()
    context = {
        'result': result,
    }
    if not result:
        return render(request, "index/error.html", context)
    return render(request, "index/result.html", context)


@login_required
def result_id(request, id):
    result = tbInfo.objects.values().filter(owner=request.user.id, id=int(id)).last()
    context = {
        'result': result,
    }
    if not result:
        return render(request, "index/error.html", context)
    return render(request, "index/result.html", context)


@login_required
def history(request):
    context = {
        "url": reverse("index_history_data"),
    }
    return render(request, "index/history.html", context)


@login_required
def history_data(request):
    page = request.GET.get('page')
    limit = request.GET.get('limit')
    all_datas = list(tbInfo.objects.values().filter(owner=request.user.id).all())
    paginator = Paginator(all_datas, limit)
    try:
        datas = paginator.page(page)
    except PageNotAnInteger:
        datas = paginator.page(1)
    except EmptyPage:
        datas = paginator.page(paginator.num_pages)
    if datas:
        for data in datas:
            data["datetime"] = data["datetime"].strftime('%Y-%m-%d %H:%M:%S')
    res = {
        "code": 0,
        "msg": "",
        "count": len(all_datas),
        "data": list(datas),
    }
    return JsonResponse(res)

# Create your views here.

