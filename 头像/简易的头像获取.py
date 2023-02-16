# -*- coding: utf-8 -*-
"""
头像获取
地址：https://www.umei.cc/touxiangtupian/katongtouxiang/
第二页地址：https://www.umei.cc/touxiangtupian/katongtouxiang/index_2.htm
"""

import requests
from lxml import etree

for i in range(11):
    if i == 0:
        url = 'https://www.umei.cc/touxiangtupian/katongtouxiang'
    else:
        url = 'https://www.umei.cc/touxiangtupian/katongtouxiang/index_{}.htm'.format(i)
    hread_url = 'https://www.umei.cc/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
    }
    response = requests.get(url=url, headers=headers)
    response.encoding = 'utf-8'
    html = etree.HTML(response.text)    
    get_divs = html.xpath('//*[@id="infinite_scroll"]')

    for son_div in get_divs:
        # 定位
        img_srcs = son_div.xpath('//*[@class="item_t"]/div/a/@href')
        img_title = son_div.xpath('//*[@class="item_t"]/div/a/img/@alt')
        for src, title in zip(img_srcs, img_title):
            urls = hread_url + src
            # 获取高清链接
            urls_response = requests.get(urls, headers=headers).text
            urls_html = etree.HTML(urls_response)
            # 定位
            get_img = urls_html.xpath('//*[@id="tsmaincont"]/div[4]/div[2]/img/@src')
            for imgs in get_img:
                # 下载高清头像
                pic_res = requests.get(imgs, headers=headers).content
                path = r'C:\Users\admin\Pictures\Saved Pictures\头像'
                with open(path + f'/{title[:6]}' + '.jpg', 'wb') as w:
                    w.write(pic_res)
