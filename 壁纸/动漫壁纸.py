# -*- coding: utf-8 -*-
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By
import requests
import os

options = webdriver.FirefoxOptions()
options.add_argument('--headless')
options.add_argument("--disable-gpu")
s = r'D:\pytest_\Case\geckodriver.exe'
driver = webdriver.Firefox(executable_path=s, options=options)
driver.get("https://desk.zol.com.cn/dongman/")
driver.find_element(By.XPATH, '//*[text()="电脑壁纸"]').click()
driver.find_element(By.XPATH, '//a[@class="sel"]').click()
driver.find_element(By.XPATH, "//ul[@class='pic-list2  clearfix']/li[3]").click()
# 切换窗口
all_value = driver.window_handles
driver.switch_to.window(all_value[-1])
sleep(0.2)


def get_url():
    for i in range(1, 11):  # 获取十组
        # 定位页数
        pages = driver.find_element(By.XPATH, "//*[@class='wrapper photo-tit clearfix']/h3/span").text
        # 获取组的名字
        titles = driver.find_element(By.XPATH, '//*[@id="titleName"]').text
        # 判断页数
        if '/' in pages[-3:-1]:
            number = int(pages[-2:-1])
            print(number)
        else:
            number = int(pages[-3:-1])
            print(number)
        # 获取地址
        for j in range(number):
            img_url = driver.find_element(By.XPATH, '//*[@id="bigImg"]').get_attribute('src')
            # 获取图片大致名称
            # img_title= driver.find_element(By.XPATH,'//*[@class="wrapper photo-tit clearfix"]/h3/span').text
            # 调用写入函数
            wirte_pic(img_url, titles + str(j))
            # 点击下一张
            driver.find_element(By.XPATH, "//a[@id='pageNext']").click()

        # 获取下一组
        driver.find_element(By.XPATH, "//*[@class='photo-set-next']/span/a").click()


def wirte_pic(url, title):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
    }
    try:
        pic_res = requests.get(url, headers=headers).content
        with open(path + title + ".jpg", 'wb') as w:
            w.write(pic_res)
        print("下载成功！{}".format(url))
    except:
        print("出了点错，跳过吧")


if __name__ == '__main__':
    path = os.getcwd() + "/电脑壁纸/"
    if os.path.isdir(path):
        print("已经存在目录，继续获取~~")
    else:
        os.mkdir('电脑壁纸')
    get_url()
