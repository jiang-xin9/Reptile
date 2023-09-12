# -*- coding: utf-8 -*-
# https://blog.csdn.net/weixin_52040868
# 公众号：测个der
# 微信：qing_an_an
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By

fox = webdriver.Firefox()
fox.get(
    "https://cn.bing.com/images/search?q=%E5%B0%8F%E4%BC%81%E9%B9%85%E8%A1%A8%E6%83%85%E5%8C%85&qpvt=%E5%B0%8F%E4%BC%81%E9%B9%85%E8%A1%A8%E6%83%85%E5%8C%85&first=1")
while True:
    down = "window.scrollTo(0, document.body.scrollHeight)"
    fox.execute_script(down)
    time.sleep(2.5)
    # 使用 JavaScript 判断是否已经滚动到底部
    is_bottom = fox.execute_script(
        'return (window.innerHeight + window.scrollY) >= document.body.offsetHeight;'
    )
    if is_bottom:
        break
eles = fox.find_elements(By.XPATH, "//*[@class='dgControl_list']")
for ele in eles:
    ele.find_element(By.XPATH, "//*[@class='mimg']").click()
    break

Frame = fox.find_element(By.XPATH, "//*[@id='OverlayIFrame']")
fox.switch_to.frame(Frame)
time.sleep(2)
num = 0
while True:
    srcs = fox.find_elements(By.XPATH, "//*[@class='imgContainer']/img")[0]
    src_ = srcs.get_attribute("src")
    res = requests.get(src_)
    with open(f"{str(num)}.jpg", "wb") as w:
        w.write(res.content)
        num += 1
    try:
        fox.find_element(By.XPATH,'//div[@id="navr"]/span').click()
    except:
        print("结束")
        fox.quit()


