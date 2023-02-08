# -*- coding: utf-8 -*-

import requests
import random
from lxml import etree
import time
import threading

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


class REQUEST_IMG:

    NUM = 0

    def run(self, url, headers):
        self.get_img(url, headers)

    def request(self, url, headers):
        """发起请求"""
        request = requests.get(url=url, headers=headers)
        html = request.content
        parse_html = etree.HTML(html)
        return parse_html

    def get_img(self, url, headers):
        """获取图片"""
        imgs = self.request(url=url, headers=headers).xpath('//div[@id="container"]/div/div/div[1]')

        for values in imgs:
            """获取图片路径"""
            pic_name = values.xpath('//div[@class="tagbqppdiv"]/a/img/@title')

            pic_img = values.xpath('//div[@class="tagbqppdiv"]/a/img')
            i = 0
            for name, img in zip(pic_name, pic_img):
                try:
                    urls = img.get('data-original')
                    """再次请求"""
                    res = requests.get(url=urls, headers=headers)
                    path = r'C:\Users\admin\Pictures\Saved Pictures\2023-2-1\{}.gif'.format(name)
                    """以二进制保存"""
                    with open(path, 'wb') as pic:
                        pic.write(res.content)
                        self.NUM += 1
                    print("爬取成功~", urls,self.NUM)
                except:
                    print("本张无法加载，PASS")


if __name__ == '__main__':
    r = REQUEST_IMG()
    s = time.time()
    threads = []

    url = r'https://www.fabiaoqing.com/biaoqing/lists/page/{}.html'
    urls = [url.format(i) for i in range(1,5)]    # 想要爬取多少页range()就改成多少
    headers = [{'User-Agent': random.choice(UA_LIST),'Referer': j} for j in urls]
    # for j in urls:
    #     header = {
    #         'User-Agent': random.choice(UA_LIST),
    #         'Referer': None}
    #     header['Referer'] = j
    #     list_header.append(header)
    # print(list_header)
    """创建线程，多线程爬取"""
    for url_, headers_ in zip(urls, headers):
        thread = threading.Thread(target=r.run, args=(url_, headers_))
        thread.start()
        threads.append(thread)
    [j.join() for j in threads]
    print("共消耗时间：", time.time() - s, "S")
