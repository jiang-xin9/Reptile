import time
import random
import requests
from concurrent.futures import ThreadPoolExecutor
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

UA_LIST = [
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11',
    'User-Agent:Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11',
    'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)',
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
]

headers = {
    "User-Agent": random.choice(UA_LIST)
}
url = f'https://wallhaven.cc/hot'
s = Service(r'D:\pytest_\Case\geckodriver.exe')
fox = webdriver.Firefox(service=s)
fox.get(url)
time.sleep(1)

def scroll():
    index = 1
    while True:
        fox.execute_script(
            'window.scrollTo(0,document.body.scrollHeight)'  # 拉动进度条，直接托到底部
        )
        if index == 1:
            pass
        else:
            try:
                WebDriverWait(fox, 12).until(
                    EC.presence_of_element_located((By.XPATH, "//*[@id='thumbs']/section[{}]/header/h2/span".format(index))))
                WebDriverWait(fox, 12).until(
                    EC.presence_of_element_located((By.XPATH, "//*[@id='thumbs']/section[{}]/header/h2".format(index))))
                num = fox.find_element(By.XPATH, "//*[@id='thumbs']/section[{}]/header/h2/span".format(index)).text
                all_num = fox.find_element(By.XPATH, "//*[@id='thumbs']/section[{}]/header/h2".format(index)).text
                print("-------{}---------{}-----------".format(num, all_num))
                if int(num) == int(all_num[-2:]):
                    break
            except:
                break
        index += 1

def request_img():
    url_ = r"https://w.wallhaven.cc/full/{}/wallhaven-{}"
    WebDriverWait(fox, 12).until(
        EC.presence_of_element_located((By.XPATH,"//img[@class='lazyload loaded']")))
    ele_img = fox.find_elements(By.XPATH,"//img[@class='lazyload loaded']")
    with ThreadPoolExecutor(max_workers=50) as pool:
        for key in ele_img:
            img_url = key.get_attribute("src")
            # print(url_.format(img_url[-13:-10], img_url[-10:]))
            pool.submit(images, url_.format(img_url[-13:-10], img_url[-10:]))
    pool.shutdown()
    fox.quit()

def images(i_url):
    result = requests.get(url=i_url,headers=headers)
    with open(r'E:\picture\wallhaven-hot/'+ i_url[-10:],'wb') as w:
        w.write(result.content)
        print("加载成功~",i_url)

if __name__ == '__main__':
    scroll()
    request_img()

