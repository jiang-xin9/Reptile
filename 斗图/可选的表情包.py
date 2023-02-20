"""
['猫咪', '狗勾', '熊猫人', '小黄脸', '高糊', '动图', '反手', '背刺', '金馆长', '动图', '单身狗', '宝宝', '文字', '熊猫人', '装逼', '文字表情', '可爱', '卡通', '小学生', '张学友', '神经猫', 'emoji', '长草', '萌萌哒', '开心果', '扔狗', 'doge', '搞笑', '妈粉', '屌丝', '搞基', '暴走', '无节操', '兔子', '回头', '逗比', '打架', '智障', '周末', '美好', '套路', '妹子', '方言', '好声音', '王锡玄', '正太', '明星表情', '猫', '宋仲基', '狗狗', '牛轰轰', '女汉子', '帅醒', '起床', '早上', '结婚', '吃', '吃货', 'gif', '动漫', '真相', '科比', '熊本熊', '女人', '妹纸', '江湖', '疾风', '围脖熊', '熊', '配字', '冷兔', '小表情', '动态', '反弹', '箭头', '猫星人', '药丸', '吃药', '有趣', '女生', '节操', '吃饼', '抖腿', '小黄人', '悟空', '芮小凸', '搞笑对话', '大佬', '明星', '有意思', '屎', '小人', '大哥', '黑鬼', '挖煤', '丢', '表哥', '电话', '嘟嘴', '辣条', '萌娃', '唐僧', 'JAKE', '哎呦熊', '皮卡丘', '记录', '作家', '复联', '蔬菜', '水果', '猥琐', '卧槽', '喵星人', '老王', '顺口溜', '隔壁', '汪蛋', '懵逼', '对方不想和你说话', 'qq', '小子', '云朵', '污', '草', '暴漫', '杀马特', '花式', '抱拳', 'sadayuki', '红内裤', '青蛙', '优衣库', '菜菜', '吻', '流氓兔', '壁咚', '猪', '友谊', '皇上', '朕', '寡人', '彼尔德', '恶搞', '尔康', '方了', '神烦狗', '赞', '猫脸', '悲伤', '唱歌', '土豪', '滑板鞋', '指人', '约', '魔性小人', '客串', '流泪', '哭', '同桌', '酚酞瓜', '喝饮料', 'sadfrog', '绿青蛙', '小熊', '滑稽', '嗷大喵', '都敏俊', '帅哥']
--------------------------------------------以上是可选的输入名称------------------------------------------------------------------
"""

# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
from lxml import etree
from concurrent.futures import ThreadPoolExecutor
from queue import Queue


class Whole:
    PATH = r'C:\Users\admin\Pictures\Saved Pictures\2023-2-9/'  # 爬取的时候更改目录
    URL = r'https://www.fabiaoqing.com/tag'
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50'}
    TITLE_List = []
    Collection_dict = {}

    def get_url(self, url_que, number):

        index_url = self.URL + '/index/page/1.html'
        request = requests.get(url=index_url, headers=self.HEADERS).text
        """使用bs4定位全部的div内的href以及title"""
        soup = BeautifulSoup(request, 'lxml')
        get_href = soup.find(id='container').find(class_='ui segment').find_all(class_='content')
        for hrefs in get_href:
            div_string = hrefs.a.string
            div_href = hrefs.a.get('href')
            # 添加进字典
            self.Collection_dict[div_string] = div_href
            self.TITLE_List.append(div_string)  # 将标题数据放入列表中

        """使用etree定位全部的a标签href以及内容"""
        x_html = etree.HTML(request)
        get_a_href = x_html.xpath('//*[@class="ui segment"]/a/@href')
        get_a_title = x_html.xpath('//*[@id="bqb"]/div/a/div/text()')
        for a_hrefs, a_titles in zip(get_a_href, get_a_title):
            # 添加进字典
            self.Collection_dict[a_titles] = [a_hrefs]
            self.TITLE_List.append(a_titles)  # 将标题数据放入列表中
        self.get_input_url(url_que, number)

    def get_input_url(self, url_que, number):
        route = self.Collection_dict[self.input_string()][4:-5]
        for url in range(1, number):
            value = self.URL + route + url_que.get()
            print("爬取中~~~")
            self.HEADERS['Referer'] = value
            request = requests.get(url=value, headers=self.HEADERS).text
            value_html = etree.HTML(request)
            div_img_href = value_html.xpath('//*[@id="bqb"]/div[2]/div/a/img/@data-original')
            div_img_title = value_html.xpath('//*[@id="bqb"]/div[2]/div/a/img/@title')
            for img_hrefs, img_titles in zip(div_img_href, div_img_title):
                self.get_img(img_hrefs, self.HEADERS, img_titles)
        print("爬取完毕~~~")

    def get_img(self, img_url, img_header, img_title):
        try:
            request = requests.get(url=img_url, headers=img_header)
            with open(self.PATH + img_title + img_url[-5:], 'wb') as w:
                print("成功 {}".format(img_url))
                w.write(request.content)
        except:
            print("这个有点问题，先跳过！！！")

    def input_string(self):
        try:
            name = input("请输出你要查找的表情包名称，例如：猫咪\n")
            print("恭喜你。有这个表情包！")
            Y_N = input("是否要爬取，请输入Y or N \n")
            if Y_N == 'y' or 'Y':
                return name
            else:
                print("害~不得劲儿，居然不爬！")
        except:
            print("没有你要找的表情包名称")

if __name__ == '__main__':
    url_que = Queue()
    w = Whole()
    number = 11     # 爬取的页数，默认10页

    for i in range(1, number):
        value = '/page/{}.html'.format(i)
        url_que.put(value)

    with ThreadPoolExecutor(max_workers=10) as threadpool:
        threadpool.submit(w.get_url, url_que, number)

