'''
Created on 2016年8月12日

@author: Administrator
'''
import requests,re,time,os,pymysql
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import selenium.webdriver.support.ui as ui
ISOTIMEFORMAT='%Y-%m-%d %X'    #Time setup



driver = webdriver.Firefox()
driver.get('https://www.zalora.com.hk/virus-arms-tote-bag-%E6%8B%BC%E8%89%B2-4584974.html')
hnadle_now = driver.current_window_handle

driver.switch_to_window(hnadle_now)
product_sku = driver.find_element_by_xpath("//td[@itemprop='sku']").text
print("product_sku:", product_sku)
