# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import threading
import time


class BS:
    NUMBER = 0
    # 如有需要直接改此处的路径即可
    PATH = r'C:\Users\admin\Pictures\Saved Pictures\2023-2-7'

    def get_info(self, url, headers):
        # 发起请求
        res = requests.get(url, headers=headers).text
        soup = BeautifulSoup(res, "lxml")
        # 定位图的位置
        divs = soup.find(id='container').find(class_='ui segment imghover').find_all(class_='tagbqppdiv')
        for values in divs:
            # 循环获取里面的图
            pic_url = values.a.img['data-original']
            pic_title = values.a.img['title']

            path = self.PATH + '\{}.{}'.format(pic_title, pic_url[-3:])
            self.img(path=path, url=pic_url, headers=headers)

    def img(self, path, url, headers):
        try:
            pic_res = requests.get(url, headers=headers)
            print("获取成功~ {}, {}".format(url, self.NUMBER))
            self.NUMBER += 1
            with open(path, 'wb') as w:
                # 保存图片
                w.write(pic_res.content)
        except:
            print("一点小插曲，跳过吧~~~")

    def pool_run(self,url, headers):
        self.get_info(url, headers)

    def run(self):
        # 运行代码，需要多少页就rang()几
        URL = r'https://www.fabiaoqing.com/biaoqing/lists/page/{}.html'
        urls = [URL.format(i) for i in range(1,5)]
        headers = [{
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
            'Referer': url
        } for url in urls]
        print("开始造图了哦~~~~")
        threads = []
        for url, header in zip(urls, headers):
            thread = threading.Thread(target=self.pool_run, args=(url, header))
            thread.start()
            threads.append(thread)
        [j.join() for j in threads]

        print("获取完毕~~~请前往 {} 查收！".format(self.PATH))


if __name__ == '__main__':
    s = time.time()
    response = BS().run()
    print("总共耗时{} s".format(time.time() - s))
