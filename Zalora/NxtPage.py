'''
Created on 2016年7月9日

@author: Administrator
'''

#爬取一个类下面的所有页，从第一页，下一页到最后一页的URL
from selenium import webdriver

URL = "https://www.zalora.com.hk/women/clothing/party-dresses/?sort=popularity&dir=desc&category_id=674"
driver = webdriver.Firefox()
driver.get(URL)

#elem = driver.find_element_by_xpath("//ul[@id='productsCatalog']")
element = driver.find_elements_by_xpath(("//a[@class='page-item selected']"))

URLlist = []
for result in element:
    URLlist.append(result)
    
    
        

