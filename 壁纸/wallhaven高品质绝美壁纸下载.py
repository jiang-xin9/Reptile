# -*- coding: utf-8 -*-
# https://blog.csdn.net/weixin_52040868
# 公众号：测个der
# 微信：qing_an_an

import requests
from lxml import etree
from concurrent.futures import ThreadPoolExecutor

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 Edg/112.0.1722.34"
}

url_list = []
def url_(num):
    url = f'https://wallhaven.cc/hot?page={num}'
    res = requests.get(url=url, headers=headers)
    res_html = etree.HTML(res.text)
    res_url = res_html.xpath("//*[@id='thumbs']/section/ul/li/figure/a/@href")
    url_list.extend(res_url)

img_list = []
def image(url):
    res_pic = requests.get(url=url, headers=headers)
    res_pic_html = etree.HTML(res_pic.text)
    res_pic_url = res_pic_html.xpath("//*[@id='main']/section/div/img/@src")
    img_list.extend(res_pic_url)

def run(value):
    value_url = requests.get(url=value, headers=headers)
    with open('report/'+value[-10:],'wb') as w:
        w.write(value_url.content)
        print("加载成功~",value)


if __name__ == '__main__':
    list(map(url_, range(1, 2)))
    list(map(image, url_list))
    with ThreadPoolExecutor(max_workers=10) as pool:
        pool.map(run, img_list)