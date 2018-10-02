# -*- coding: utf-8 -*-
'''
Created on 2016年11月01日
Input is the top category URL. Output is product URL of each product.
@author: Administrator
'''

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException    

def check_exists_by_xpath(driver, xpath):
    try:
        driver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False
    return True
 
def crawl_product_URL(top_category_url):
    current_URL = top_category_url
    driver = webdriver.Firefox()
#     driver = webdriver.PhantomJS()
    
    while 1:
        driver.get(current_URL)
        #WebDriverWait(driver, 3)
         
        if not check_exists_by_xpath(driver, '//section[@class="catalog-box"]'):
            return
         
        try:
            if check_exists_by_xpath(driver, '//div[@class="eg-close-step-1 eg-invisibleButton"]'):
                driver.find_element_by_xpath('//div[@class="eg-close-step-1 eg-invisibleButton"]').click()
        except:
            print('nothing')
            
        item_list = driver.find_elements_by_xpath(("//div[@class='b-catalogList__itm js-catalogList__itm hasOverlay unit size1of3']"))
        for items in item_list:
            with open('C:/Users/Administrator/Desktop/zalora_URLs.txt','a', encoding="utf8") as f:
                f.write(items.find_element_by_xpath("li/a").get_attribute("href") + '\n')
        
        try:
            nextPage = driver.find_element_by_xpath('//*[@id="topPagination"]/div/ul/li[3]/a[@title="Next"]')
        except:
            return
             
        try:
            if nextPage is not None:
                if current_URL != nextPage.get_attribute('href'):
                    current_URL = nextPage.get_attribute('href')
                else:
                    return
            else:
                return
        except:
            return
    driver.quit()
 
top_category_URL = open("C:/Users/Administrator/Desktop/zalora_top_category.txt")
lines = top_category_URL.readlines()
top_category_URL.close()
 
start_page_No = 1
for line in lines:
    print(start_page_No, line)
    line = line.strip('\n')
    crawl_product_URL(line)
    start_page_No = start_page_No + 1

