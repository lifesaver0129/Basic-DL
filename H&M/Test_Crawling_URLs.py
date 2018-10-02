'''
Created on 2016年9月22日
测试H&M 加载按钮。
@author: Administrator
'''


from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from _overlapped import NULL
import os, re, requests
from selenium.common.exceptions import NoSuchElementException    
from selenium.webdriver.common.action_chains import ActionChains


urlstring = 'http://www.hm.com/hk/en/products/ladies'
# urlstring = 'http://www.hm.com/hk/en/products/ladies/tops/short_sleeved'
driver = webdriver.Firefox()

driver.get(urlstring)


view_more_button = driver.find_element_by_xpath("//button[@class='load-more-btn js-product-list-load-more']")

while view_more_button.is_enabled():
    view_more_button.click()
    
#find all items
items = driver.find_elements_by_xpath("//div[@class='product-list-item']/div/div/a")
f = open('C:/Users/Administrator/Desktop/urls.txt', 'w')

for ele in items:
    print(ele.get_attribute("href"))
    f.write(str(ele.get_attribute("href")) + '\n')
    
f.close()


driver.quit()