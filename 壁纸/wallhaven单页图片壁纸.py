import requests
from lxml import etree
from concurrent.futures import ThreadPoolExecutor

url = 'https://wallhaven.cc/hot?page=5'

"""先看看能不能爬"""

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 Edg/112.0.1722.34"
}
res = requests.get(url=url, headers=headers)

# //*[@id='thumbs']/section/ul/li/figure/img    定位元素
res_html = etree.HTML(res.text)
res_jpg = res_html.xpath("//*[@id='thumbs']/section/ul/li/figure/img/@data-src")
# print(len(res_jpg),res_jpg)
"""下载HTML"""

def run(value):
    value_url = requests.get(url=value, headers=headers)
    with open(value[-10:],'wb') as w:
        w.write(value_url.content)
        print("加载成功~",value_url)

"""请求响应有点慢，导致下载有点慢(requests搞不定)，只能通过其他手段提升一下速度---多线程"""

if __name__ == '__main__':
    with ThreadPoolExecutor(max_workers=10) as pool:
        pool.map(run, res_jpg)