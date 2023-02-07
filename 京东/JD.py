# -*- coding: utf-8 -*-

from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By


class JD:
    def __init__(self):
        # 火狐无头模式
        self.options = webdriver.FirefoxOptions()
        self.options.add_argument('--headless')
        self.options.add_argument("--disable-gpu")
        s = r'D:\pytest_\Case\geckodriver.exe'
        self.driver = webdriver.Firefox(executable_path=s, options=self.options)
        self.i = 0  # 计数

    def get_html(self):
        # 打开网页搜索书籍
        self.driver.get('https://www.jd.com/')
        self.driver.find_element_by_xpath('//*[@id="key"]').send_keys("python")
        self.driver.find_element_by_xpath("//*[@class='form']/button").click()

    def get_data(self):
        while True:
            self.driver.execute_script(
                'window.scrollTo(0,document.body.scrollHeight)'  # 拉动进度条，直接托到底部
            )
            sleep(2)
            list_ = self.driver.find_elements(By.CLASS_NAME, 'gl-item')     # 定位爬取的标签列表
            for value in list_:
                dict_ = {}
                dict_["价钱"] = value.find_element_by_xpath(".//div[@class='p-price']/strong/i").text + '元'
                dict_["描述"] = value.find_element_by_xpath(".//div[@class='p-name p-name-type-2']/a/em").text
                dict_["评论数"] = value.find_element_by_xpath(
                    ".//div[@class='p-commit']/strong/a|.//div[@class='p-commit']/strong").text
                dict_["出版社"] = value.find_element_by_xpath(".//div[@class='p-shop']").text
                self.i += 1
                print(dict_)
            # 获取当前页数
            res = self.driver.find_element(By.XPATH, '//span[@class="p-skip"]/input').get_attribute('value')
            print("*"*20,res)
            # 获取总页数
            sum_res = self.driver.find_element(By.XPATH, '//span[@class="p-skip"]/em/b').text
            if res != sum_res:      # 判断页数
                self.driver.find_element(By.XPATH, '//*[text()="下一页"]').click()
                sleep(0.5)
            else:
                print("已经到头了，结束爬取")
                break


    def run(self):
        self.get_html()
        self.get_data()
        print("次数：{}".format(self.i))


jd = JD()
jd.run()
