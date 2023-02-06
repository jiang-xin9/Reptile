# -*- coding: utf-8 -*-

from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By


class JD:
    def __init__(self):
        self.options = webdriver.FirefoxOptions()
        self.options.add_argument('--headless')
        self.options.add_argument("--disable-gpu")
        s = r'D:\pytest_\Case\geckodriver.exe'
        self.driver = webdriver.Firefox(executable_path=s, options=self.options)
        self.i = 0

    def get_html(self):
        self.driver.get('https://www.jd.com/')
        self.driver.find_element_by_xpath('//*[@id="key"]').send_keys("python")
        self.driver.find_element_by_xpath("//*[@class='form']/button").click()

    def get_data(self):
        self.driver.execute_script(
            'window.scrollTo(0,document.body.scrollHeight)'  # 拉动进度条
        )
        sleep(2)
        list_ = self.driver.find_elements(By.CLASS_NAME, 'gl-item')
        for value in list_:
            dict_ = {}
            dict_["价钱"] = value.find_element_by_xpath(".//div[@class='p-price']/strong/i").text + '元'
            dict_["描述"] = value.find_element_by_xpath(".//div[@class='p-name p-name-type-2']/a/em").text
            dict_["评论数"] = value.find_element_by_xpath(
                ".//div[@class='p-commit']/strong/a|.//div[@class='p-commit']/strong").text
            dict_["出版社"] = value.find_element_by_xpath(".//div[@class='p-shop']").text
            self.i += 1
            print(dict_)

    def run(self):
        self.get_html()
        self.get_data()
        print("次数：{}".format(self.i))


jd = JD()
jd.run()