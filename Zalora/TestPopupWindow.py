'''
Created on 2016年8月11日

@author: Administrator
'''
import requests,re,time,os,pymysql
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
ISOTIMEFORMAT='%Y-%m-%d %X'    #Time setup


driver = webdriver.PhantomJS('phantomjs')
driver.get('https://www.zalora.com.hk/playboy-playboy-backpack-%E8%97%8D%E8%89%B2-4573257.html')
print(driver.title)
print(driver.current_url)

'''
driver = webdriver.Firefox()
driver.get('https://www.zalora.com.hk/playboy-playboy-backpack-%E8%97%8D%E8%89%B2-4573257.html')

click_the_window = driver.find_element_by_xpath('//div[@class="eg-step eg-step-1"]/a/div')
click_the_window.click()

driver.switch_to_window(driver.window_handles[-1])
title=driver.title
'''
driver.close()


