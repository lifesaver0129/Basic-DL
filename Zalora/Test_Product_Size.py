'''
Created on 2016年8月8日

@author: Administrator
'''
# sizeSystem:size:desc
# EU:36:Only 4 items in stock
# ::Only 4 items in stock



from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException    


def count_web_elements(driver,id):
    number = 0
    element = driver.find_elements_by_xpath(id)
    for ele in element:
        number = number + 1
    return number


driver = webdriver.Firefox()

currentPageURL = "https://www.zalora.com.hk/carlton-london-perforated-ballerinas-%E6%A3%95%E8%89%B2-4588523.html"
#currentPageURL = "https://www.zalora.com.hk/rawrow-rugged-canvas-laptop-backpack-%E7%99%BD%E8%89%B2-4619599.html"
#currentPageURL = "https://www.zalora.com.hk/cotton-on-skinny-straight-jeans-%E8%97%8D%E8%89%B2-4628054.html"
#currentPageURL = "https://www.zalora.com.hk/xixili-vanessa-sleepwear-%E7%B2%89%E7%B4%85%E8%89%B2-4556165.html"
driver.get(currentPageURL)

#关闭跳出窗口
modal = driver.find_element_by_xpath('//div[@class="eg-close-step-1 eg-invisibleButton"]')
if modal is not None:
    modal.click()
else:
    print('Page not found')

# product size aviliable
#有好几种情况，第一种情况，有两个下拉框；第二种情况没有下拉框；第三种情况，只有一个下拉框
product_stock = ''
size_system = driver.find_elements_by_xpath('//div[@class="prd-option-collection prdSizeOption box size"]/select')
#num_select is the number of select tag, the number could be 0,1,2;
#calculate the number of num_select
num_select = count_web_elements(driver,'//div[@class="prd-option-collection prdSizeOption box size"]/select')
if num_select == 2:
    for ele_size_system in driver.find_elements_by_xpath('//select[@class="prdSizeOption__sizeSystem"]/option'):
        #check if the option is clickable
        if ele_size_system.is_enabled():
            ele_size_system.click()
            prdSizeOption = driver.find_element_by_xpath('//select[@class="js-subSelect prdSizeOption__sizeDetail "]')
            for ele_prdSizeOption in prdSizeOption.find_elements_by_tag_name('option'):
                #check if the option is clickable
                if ele_prdSizeOption.is_enabled():
                    ele_prdSizeOption.click()
                    #print(ele_prdSizeOption.text)
                    user_selection = driver.find_element_by_xpath('//span[@id="product-option-stock-number"]')
                    product_stock = product_stock + ele_size_system.text + ':' + ele_prdSizeOption.text + ',' + user_selection.text + ';'
                    #print(user_selection.text)
    print(product_stock)
if num_select == 1:
    for ele_size_system in driver.find_elements_by_xpath('//div[@class="prd-option-collection prdSizeOption box size"]/select/option'):
        #check if the option is clickable
        if ele_size_system.is_enabled():
            ele_size_system.click()
            user_selection = driver.find_element_by_xpath('//span[@id="product-option-stock-number"]')
            product_stock = product_stock + ele_size_system.text + ':' + user_selection.text + ';'
    print(product_stock)
if num_select == 0:
    size_system = driver.find_element_by_xpath('//div[@class="prd-option-collection prdSizeOption box size"]')
    product_stock = product_stock + size_system.text + ';'
    product_option_stock_hint = driver.find_element_by_xpath('//span[@id="product-option-stock-number"]')
    product_stock = product_stock + product_option_stock_hint.text
    print(product_stock)

driver.quit()

