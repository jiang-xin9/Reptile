# -*- coding: utf-8 -*-

"""
玄幻小说人气排行
https://www.bbiquge.net/fenlei/1_1/
"""

import requests
from lxml import etree
import os
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor


Book_chapter_dic = {}


def GET_ALL_BOOK_INFO(BOOK_NAME):
    url = 'https://www.bbiquge.net/fenlei/1_1/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
    }
    resquest = requests.get(url=url, headers=headers)
    resquest.encoding = 'gbk'
    Html = etree.HTML(resquest.text)
    # 获取书名
    Author = Html.xpath("//*[@class='visitlist']/ul/li/span/a/text()")
    # 获取链接
    Author_url = Html.xpath("//*[@class='visitlist']/ul/li/span/a/@href")
    # 获取作者
    Book_title = Html.xpath("//*[@class='sp_xinxi']/text()")
    for author, author_utl in zip(Author, Author_url):
        Book_chapter_dic[author] = author_utl
    try:
        print("获取书籍信息：",BOOK_NAME, Book_chapter_dic[BOOK_NAME])
        for page in range(1, 26):
            if page == 1:
                put_url = Book_chapter_dic[BOOK_NAME]
            else:
                put_url = Book_chapter_dic[BOOK_NAME] + "/index_{}.html".format(page)
            GET_BOOK(put_url, headers, BOOK_NAME)
    except:
        print("没有所需要的书籍！请查看玄幻小说人气排行中名称")


def GET_BOOK(url, headers, BOOK_NAME):
    resquest = requests.get(url=url, headers=headers)
    resquest.encoding = 'gbk'
    Html = etree.HTML(resquest.text)
    # 获取总共多少页
    Get_pages = Html.xpath('//*[@class="zjbox"]/div/select/option/text()')
    # print(Get_pages[-1][1:3])
    # 获取书籍章节链接
    Book_chapter = Html.xpath('//*[@class="zjbox"]/dl/dd/a/@href')
    # 获取书籍目录信息
    Book_chapter_title = Html.xpath('//*[@class="zjbox"]/dl/dd/a/text()')
    for chapter, chapter_title in zip(Book_chapter, Book_chapter_title):
        URL = Book_chapter_dic[BOOK_NAME] + chapter
        # print(URL, chapter_title)
        write(URL, headers, chapter_title)

def write(url, headers, title):
    res = requests.get(url, headers=headers)
    res.encoding = 'gbk'
    soup = BeautifulSoup(res.text, 'lxml')
    BOOK = soup.find(id='content')
    # print(BOOK.text)
    with open(path + '/{}'.format(title) + '.txt', 'w',encoding='utf-8') as w:
        w.write(BOOK.text.replace(' ','\r'))
    print("下载成功！{}".format(title))


if __name__ == '__main__':
    path = os.getcwd() + "/小说"
    if os.path.isdir(path):
        print("已经存在目录，继续获取~~")
    else:
        os.mkdir('小说')
    name = input("请输入获取书籍名字：\n")
    with ThreadPoolExecutor(max_workers=10) as pool:
        pool.submit(GET_ALL_BOOK_INFO, name)

