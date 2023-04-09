import requests
from lxml import etree
from concurrent.futures import ThreadPoolExecutor
from queue import Queue

url = 'http://touxiangkong.com/katong/qinglv/'

header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:100.0) Gecko/20100101 Firefox/100.0"
}

# 发起请求 检查一下
reslut = requests.get(url=url, headers=header)
reslut.encoding = 'utf-8'

"""请求正常，看看元素图片"""
html = etree.HTML(reslut.text)
get_url = html.xpath('//*[@class="excerpts-wrapper"]/div/article/a/@href')        # 取值src

def pachong():
    url_ = 'http://touxiangkong.com'
    # 循环发起请求，将一整个界面的全部拿到
    for url_value in get_url:
        get_url_reslut = requests.get(url=url_ + url_value, headers=header)
        get_url_reslut.encoding = 'utf-8'
        url_html = etree.HTML(get_url_reslut.text)
        get_url_ = url_html.xpath('//*[@class="content-wrap"]/div/article/div/div/div/div/p/img/@src')        # 取值src
        for url in get_url_:
            q.put(url)


def request_url():
    # 下载
    # 对图片地址再次发起请求
    while not q.empty():
        url = q.get()
        img_result = requests.get(url=url, headers=header)
        with open('满满的情头/' + url[-15:], 'wb') as w:
            w.write(img_result.content)
            print("加载成功~", url)


if __name__ == '__main__':
    import time
    q = Queue()
    pachong()
    """有点慢。加快一下获取速度"""
    start = time.time()
    with ThreadPoolExecutor(max_workers=50) as pool:
        for value in range(50):
            pool.submit(request_url)
    pool.shutdown()
    print("总耗时：",time.time() - start)