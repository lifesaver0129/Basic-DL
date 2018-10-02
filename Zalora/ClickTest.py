'''
Created on 2016年7月10日

@author: Administrator
'''


from selenium import webdriver
from setuptools.package_index import HREF
from _overlapped import NULL


driver = webdriver.Firefox()


currentPageURL = "https://www.zalora.com.hk/women/clothing/dresses/?from=header"
driver.get(currentPageURL)

#elem = driver.find_element_by_xpath("//ul[@id='productsCatalog']")

element = driver.find_elements_by_xpath(("//div[@id='topPagination']"))

#写入txt文件
for result in element:
    #detailsPage是当前页page-item selected
    thisPage = result.find_element_by_xpath("//a[@class='page-item selected']").get_attribute("href")
    print(thisPage)
    print('***************')
    #detailsPage是当前页page-item next
    print(result.find_element_by_xpath("//a[@title='Next']").get_attribute("href"))
    nextPage = result.find_element_by_xpath('//*[@id="topPagination"]/div/ul/li[3]/a[@title="Next"]')
    
    if nextPage is not NULL:
        currentPageURL = nextPage
        nextPage.click()
    elif nextPage is NULL:
        break
    print(nextPage)  
    
driver.close()
