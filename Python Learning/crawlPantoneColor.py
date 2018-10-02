#coding=utf-8

from selenium import webdriver
import os, time, queue, urllib
ISOTIMEFORMAT='%Y-%m-%d %X'    #Time setup



pantoneColors = open("C:/Users/Administrator/Desktop/pantonecolor.txt", encoding='utf8').readlines()

pantoList = []
for ele in pantoneColors:
    ele = ele.strip('\n')
    elelist = ele.split('\t')
    pantoList.append(elelist[1])



startURL = 'https://www.pantone.com/color-finder?q='

for pantone in pantoList:
#     searchField = driver.find_element_by_id('color-input-fields')
#     
#     inputElement = searchField.find_element_by_class_name('searchterm')
#     inputElement.send_keys(pantone)
#     
#     clickbutton = searchField.find_element_by_id('submit-color-search')
#     clickbutton.click()
# 
#     driver.implicitly_wait(3)
    print(pantone)
    try:
        driver = webdriver.PhantomJS()
        URL = startURL + pantone
        driver.get(URL)

        pantoneRGB = driver.find_element_by_class_name('coloredSquare').get_attribute('style')
        pantoneName = driver.find_element_by_xpath("//div[@class='pColorCode']").text
        
        with open('C:/Users/Administrator/Desktop/pantoneColorTEST.txt','a', encoding='utf8') as f:
            f.write(pantone + '\t' + pantoneRGB + '\t' + pantoneName + '\n')
        driver.close()
        
    except:
        with open('C:/Users/Administrator/Desktop/pantoneColorTEST.txt','a', encoding='utf8') as f:
            f.write(pantone + '\n')
        driver.close()
    
    
    