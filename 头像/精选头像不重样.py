# -*- coding: utf-8 -*-
# https://blog.csdn.net/weixin_52040868
# 公众号：测个der
# 微信：qing_an_an
# -*- coding: utf-8 -*-
# https://blog.csdn.net/weixin_52040868
# 公众号：测个der
# 微信：qing_an_an

import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
import random

HREF_URLS = []
IMG_URLS = []
UA_LIST = [
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11',
    'User-Agent:Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11',
    'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)',
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
]

headers = {
    "User-Agent": random.choice(UA_LIST),
}
def request():
    URL = 'https://www.ddtouxiang.com'
    html = requests.get(URL,headers=headers)
    html.encoding = 'utf-8'

    soup = BeautifulSoup(html.text,'lxml')
    HREFS = soup.findAll(class_='index_tx_item_title')
    # print(HREFS)
    for value in HREFS:
        A_HREF = value.find('a')
        HREF_URLS.append(URL+A_HREF.get('href'))

    for IMG_URL in HREF_URLS[:5]:
        IMG_HTML = requests.get(IMG_URL,headers=headers)
        IMG_HTML.encoding = 'utf-8'
        IMG_SOUP = BeautifulSoup(IMG_HTML.text,'lxml')
        IMG_SRC = IMG_SOUP.findAll('img',class_='detail_picbox_img')
        for src in IMG_SRC:
            IMG_URLS.append(src.get('src'))

def run(url):
    header = {
        "User-Agent": random.choice(UA_LIST),
        'Referer': url
    }
    path = r"E:\picture\精选头像\\"
    pic = requests.get(url,headers=header)
    pic.encoding = 'utf-8'
    print(path + url[-10:])
    with open(path + url[-10:],'wb') as w:
        w.write(pic.content)
        print("加载成功—",url)


if __name__ == '__main__':
    request()
    print(IMG_URLS)
    with ThreadPoolExecutor(max_workers=50) as pool:
        pool.map(run, IMG_URLS)
