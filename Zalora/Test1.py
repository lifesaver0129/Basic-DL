'''
Created on 2016年8月2日

@author: Administrator
'''

from selenium import webdriver
import time
from _overlapped import NULL
from selenium.common.exceptions import NoSuchElementException
import codecs



def crawlURL(driver):
    productList = driver.find_elements_by_xpath('//ul[@id="srplist"]/li')
    for ele in productList:
        productURL = ele.find_element_by_xpath('div/a').get_attribute("href").split('\'')
        #print(productURL[1])
        productcontent.write(productURL[1] + '\n')
    print(len(productList))


start_URL = 'http://glistings.gmarket.co.kr/Listview/List?keyword=&GdlcCd=100000003&GdmcCd=200000498&GdscCd=300004673&type=IMG&pagesize=650&ordertype=&IsOversea=False&IsDeliveryFee=&IsGmarketBest=&IsGmileage=False&IsDiscount=False&IsGstamp=False&IsBookCash=False&DelFee=&page=1&IsFeature=&IsGlobalSearch=undefined'
driver = webdriver.Firefox()
driver.get(start_URL)
time.sleep(10)

productcontent = codecs.open("productcontent.txt", "w", "utf-8")
pagestart = 1
while driver is not NULL:
    print('page ', pagestart, ': ', driver.current_url)
    crawlURL(driver)
    nextPage = driver.find_element_by_xpath('//a[@class="cpp_icon btn_next"]')
    lastPage = driver.find_element_by_xpath('//a[@class="cpp_icon btn_last"]')
    if nextPage != lastPage:
        nextPage.click()
    pagestart = pagestart + 1
    time.sleep(10)
    
productcontent.close()

# driver.close()
