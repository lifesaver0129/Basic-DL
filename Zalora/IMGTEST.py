'''
Created on 2016年7月13日

@author: Administrator
'''
import re
import requests

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
import csv,os
from cgitb import text
from click.types import Path

path = 'C:/Users/Administrator/Desktop/ZA919AA35BOASG'
driver = webdriver.Firefox()
driver.get('https://www.zalora.com.hk/zalora-checks-long-sleeve-shirt-%E9%BB%91%E8%89%B2-4540608.html')

#关闭跳出窗口
modal = driver.find_element_by_xpath('//div[@class="eg-close-step-1 eg-invisibleButton"]')
if modal is not None:
    modal.click()


img_list = driver.find_elements_by_xpath('//ul[@class="prd-moreImagesList ui-listItemBorder ui-listLight swiper-wrapper"]/li')
imgnum = 1

img_url_list = []
for imageElement in img_list:
    image_url = imageElement.get_attribute("data-image-big")
    img_url_list.append(image_url)
i = 1
while i <  len(img_url_list):
    image_url = img_url_list[i]
    print(image_url)
    print(imgnum)
    if not os.path.exists(path):  ###判断文件是否存在，返回布尔值
        os.makedirs(path)
    img_postfix = re.search(r'(\.jpg|\.png)$', str(image_url))
    save_path = path + '/' + str(imgnum) + str(img_postfix.group())
    print(save_path)
    r = requests.get(image_url, stream=True)
    with open(save_path, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)
                f.flush()
    imgnum = imgnum + 1
    i = i + 1
    f.close()