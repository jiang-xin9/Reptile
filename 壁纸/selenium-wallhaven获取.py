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


def get_img():
    original_window = fox.current_window_handle
    ele = fox.find_elements(By.XPATH, "//a[@class='preview']")
    for value in ele:
        value_url = value.get_attribute("href")
        fox.execute_script("window.open('{}')".format(value_url))
        for window_handle in fox.window_handles:
            if window_handle != original_window:
                fox.switch_to.window(window_handle)
                break
        try:
            WebDriverWait(fox, 5).until(
                EC.presence_of_element_located((By.XPATH, "//*[@id='wallpaper']")))
            img = fox.find_element(By.XPATH, "//*[@id='wallpaper']").get_attribute('src')
            img_list.append(img)
            with open("img_url.txt", 'a', encoding='utf-8') as w:
                w.write(img + '\n')
            print(img)
        except:
            pass
        # 关闭新窗口
        fox.close()
        # 切换回原始窗口
        fox.switch_to.window(original_window)

    fox.quit()

def images(url):
    result = requests.get(url=url,headers=headers)
    with open('report/'+url[-10:],'wb') as w:
        w.write(result.content)

if __name__ == '__main__':

    img_list = []
    scroll()
    with ThreadPoolExecutor(max_workers=10) as img_pool:
        img_pool.submit(get_img)

    with ThreadPoolExecutor(max_workers=10) as img_pool:
        img_pool.map(images, img_list)
    img_pool.shutdown()
