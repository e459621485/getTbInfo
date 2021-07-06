import requests
import re
import json
import time
import urllib.parse
from index.models import tbInfo


requests.packages.urllib3.disable_warnings()
req_session = requests.Session()


def search():
    url = 'https://item.taobao.com/item.htm?spm=a21bo.21814703.201876.27.5af911d9kf25lK&id=539707527654&scm=1007.34127.227518.0&pvid=a52aaedd-dfc5-456f-9877-c9e043c57cda'
    # url = 'https://detail.tmall.com/item.htm?id=573702103280&spm=a21bo.21814703.201876.13.5af911d9jmQxBQ&scm=1007.34127.211940.0&pvid=631096de-6a1a-4aff-b0a2-6a8e7713305d'
    headers = {
        'referer': 'https://www.taobao.com/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }
    response = req_session.get(url, headers=headers, verify=False, timeout=5)
    response_text = response.text.replace('\n', '').replace('\r', '').replace(" ", '')
    # print(response.text)
    s = '<strong id="J_StrPrice"><em class="tb-rmb">&yen;</em><em class="tb-rmb-num">58.00</em></strong>'
    if "taobao" in url:
        goods_match = re.search(r'item:{(.*?)},', response_text)
        response_text = goods_match.group(1)
        print(goods_match.group(1))
        title = re.search(r"title:'(.*?)',", response_text).group(1).encode('latin-1').decode('unicode_escape')
        img = re.search(r"pic:'(.*?)',", response_text).group(1)
        price = re.search(r'tb-rmb-num">(.*?)<', response.text).group(1)
        seller = re.search(r"sellerNick:'(.*?)',", response_text).group(1)
    elif "tmall" in url:
        goods_match = re.search(r'"itemDO":{(.*?)}', response.text)
        data = json.loads('{' + goods_match.group(1) + '}')
        title = data['title']
        price = data['reservePrice']
        seller = urllib.parse.unquote(data['sellerNickName'])
        img = re.search(r'.*J_ImgBooth"\s.*src="(.*?)"', response.text).group(1)



# search()

list = tbInfo.objects.values().all()
print(list)