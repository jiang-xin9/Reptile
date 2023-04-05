import requests
from lxml import etree

url = 'http://touxiangkong.com/katong/qinglv/'
index = 'http://touxiangkong.com'
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
}


def request(url):
    result = requests.get(url=url, headers=headers)
    result.encoding = 'utf-8'
    return result


def start_request():
    result = request(url)
    html = etree.HTML(result.text)
    get_html_href = html.xpath('//*[@class="excerpts-wrapper"]/div/article/a/@href')
    url_list = []
    for other_url in get_html_href[:3]:  # 如果想获取本html中的全部，那就把[:3]去掉
        index_url = index + other_url
        url_list.append(index_url)
    get_url(url_list)


def get_url(url_list):
    for html_value in url_list:
        other_result = request(html_value)
        other_html = etree.HTML(other_result.text)
        get_other_href = other_html.xpath('//*[@class="content-wrap"]/div/article/div/div/div/div/p/img/@src')
        num = 0
        for img_url in get_other_href:
            img_request = requests.get(url=img_url, headers=headers).content
            with open(f'情头{num}.jpg', 'wb') as w:
                w.write(img_request)
                print("下载成功~ {}".format(img_url))
                num += 1


if __name__ == '__main__':
    start_request()
