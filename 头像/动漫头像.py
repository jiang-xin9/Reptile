# -*- coding: utf-8 -*-
"""
因网站做了限制，前面会多线程，后面只能一张一张爬
"""

import requests
from lxml import etree
from concurrent.futures import ThreadPoolExecutor
import os
import time


def get_img_url(headers):
    for i in range(1,11):
        if i == 1:
            url = 'https://www.umei.cc/touxiangtupian/katongtouxiang'
        else:
            url = 'https://www.umei.cc/touxiangtupian/katongtouxiang/index_{}.htm'.format(i)
        response = requests.get(url=url, headers=headers)
        response.encoding = 'utf-8'
        html = etree.HTML(response.text)
        get_href = html.xpath('//*[@id="infinite_scroll"]/div/div/div/a/img/@data-original')
        get_title = html.xpath('//*[@id="infinite_scroll"]/div/div/div/a/img/@alt')
        writer_img(get_href, get_title, headers)


def writer_img(urls, titles, headers):
    for href, title in zip(urls, titles):
        try:
            pic_res = requests.get(href, headers=headers).content
            with open(path + f'/{title[1:10]}' + ".jpg", 'wb') as w:
                w.write(pic_res)
            print("下载成功！{}".format(href))
        except:
            print("出了点错，跳过吧")


if __name__ == '__main__':
    path = os.getcwd() + "/情头"
    if os.path.isdir(path):
        print("已经存在目录，继续获取~~")
    else:
        os.mkdir('情头')
    s = time.time()

    headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
        }
    with ThreadPoolExecutor(max_workers=10) as pool:
        pool.submit(get_img_url, headers)
    print("总耗时{} s".format(time.time() - s))

