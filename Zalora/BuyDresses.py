'''
Created on 2016年4月6日

@author: uestcdengww
'''
# -*- coding: UTF-8 -*-

import re
import time
from selenium.common.exceptions import NoSuchElementException    
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import chardet
import urllib.request, urllib.parse, urllib.error
import os

class BuyDressesSpider:

    def __init__(self,save_path):
        self.save_path = save_path
        self.driver = webdriver.Firefox()  # 调用Firefox浏览器
        # self.iedriver = "C://Program Files//Internet Explorer//IEDriverServer.exe"
        # os.environ["webdriver.ie.driver"] = self.iedriver
        # self.driver = webdriver.Ie(self.iedriver)

    # 传入图片地址，文件名，保存单张图片
    def saveImg(self, imageURL, save_path, fileName):
        try:
            # NOTE the stream=True parameter
            r = requests.get(imageURL, stream=True)
        except  Exception as e:
            print("---@(saveImg)@--Get and save this image Failed !")
            print(e)
            return None
        else:
            image_name = save_path + '/' + fileName
            print(("---------正在保存图片%s......" % fileName))
            with open(image_name, 'wb') as f:
                for chunk in r.iter_content(chunk_size=1024):
                    if chunk:  # filter out keep-alive new chunks
                        f.write(chunk)
                        f.flush()
            f.close()
            return image_name

    # 保存多张写真图片
    def saveImgs(self, imagesURL, save_path, name):
        index = 0
        print(("----$$开始爬取%s的图片......\n" % name))
        for imgURL in imagesURL:
            imageurl = re.match(r'http://(.+)(\.jpg|\.png)', imgURL)
            if imageurl is not None:
                img_postfix = re.search(r'(\.jpg|\.png)$', str(imgURL))
                if img_postfix is not None:
                    fileName = name + str(index) + img_postfix.group()
                    self.saveImg(imageurl.group(), save_path, fileName)
                    index += 1
        return index
    
    def validateFileName(self, fileName):  # 过滤文件名,返回合法文件名 
        rstr = r"[\/\\\:\*\?\"\<\>\|]"  # '/\:*?"<>|'
        new_name = re.sub(rstr, "-", fileName)
        return new_name

    # 创建新目录
    def mkdir(self, path):
            path = path.strip()
            isExists = os.path.exists(path)
            # 判断路径是否存在
            if not isExists:
                # 如果不存在，则创建目录
                os.makedirs(path)
            else:
                # 如果目录存在，则不创建，并提示目录已存在
                print((path, '文件夹已经存在'))
            return path
        
    def getSizeDetailsAndSave(self,driver,save_path,name): 
        try:
            sizeDetails = driver.find_element_by_id("sizeDetails")
        except NoSuchElementException as e:
            print("---@ getSizeDetailsAndSave()@--Unable to locate element sizeDetails !")
            print(e)
            return None
        else:
            try:
                size__measurement = sizeDetails.find_element_by_class_name("size__measurement")
                measurement = size__measurement.find_element_by_tag_name("span").get_attribute("innerHTML") + "<br><br>"
            except NoSuchElementException as e:
                print("---@ getSizeDetailsAndSave()@--Unable to locate element size__measurement !")
                print(e)
                measurement = ""
            try:
                    
                size__attributes = sizeDetails.find_element_by_class_name("size__attributes")
                attributes = size__attributes.find_element_by_class_name("mbm").get_attribute("innerHTML") + "<br>" + size__attributes.find_element_by_class_name("mtm").get_attribute("innerHTML") + "<br><br>" + size__attributes.find_element_by_class_name("mrm").get_attribute("innerHTML") + "<br>" + size__attributes.find_element_by_xpath("//*[@id='sizeDetails']/div[2]/span[3]").get_attribute("innerHTML")
            except NoSuchElementException as e:
                print("---@ getSizeDetailsAndSave()@--Unable to locate element size__attributes !")
                print(e)
                attributes = ""
            #driver.find_element_by_id("sizeDetails")
            #size__attributes = driver.find_element_by_xpath(u'/div[@class="size__attributes unit size1of3 box"]/span').text
            Details = measurement + attributes
            Details = re.sub(r"<br>", "\\r\\n", Details)
            detailsFileName = save_path + '/' + name + "-details.txt"
            f = open(detailsFileName, "w+", encoding='utf-8')
            print(("----$$正在保存%s的productDetails....." % name))
            # print(self.driver.page_source)
            print("***sizeDetails: ",Details)
            # info=individualResume.get_attribute("outerHTML")
            f.write(str(Details))
            f.close()
            
    def getImageandSave(self, driver, productMainPages):
        #productsImageURLs = []
        for productDetailsPage in productMainPages: 
            print("爬取：", productDetailsPage)
            driver.get(productDetailsPage)
            #time.sleep(1)
            #创建该product的文件夹，用于存放照片和details
            #name = driver.find_element_by_tag_name("title").text
            name = driver.title
            print("name: ",name)
            name = self.validateFileName(name)
            save_path = self.save_path + name
            print("&&创建目录：",save_path)
            self.mkdir(save_path)
            self.getSizeDetailsAndSave(driver, save_path, name)
                
            #imagesURL = []
            index = 0
            for imageElement in driver.find_elements_by_class_name("product__otherImage"):
                image_url = imageElement.get_attribute("data-image-big")
                image = re.match(r'http://(.+)(\.jpg|\.png)', image_url)
                if image is not None:#问题所在
                    #img_postfix = re.search(r'(\.jpg|\.png)$', str(image_url))
                    img_postfix = image.group(2)
                    if img_postfix is not None:
                        #fileName = str(index) + img_postfix.group()
                        fileName = str(index) + img_postfix
                        self.saveImg(image_url, save_path, fileName)
                        index += 1
                #imagesURL.append(image_url)
            #self.saveImgs(imagesURL, save_path, "")
            #productsImageURLs.append(imagesURL)
        # ImageURLs[0] = driver.title#第一个元素为页面名称
        #return productsImageURLs
    
    def main(self, save_path, startPage=1, deepth=2):
        self.driver.get('http://www.zalora.com.hk/women/clothing/dresses/?noWT=1') #爬取起始页面
        modal = self.driver.find_element_by_xpath('//*[@id="evergage-tooltip-ambiKWoo"]/a')
        if modal is not None:
            modal.click()
            nextPage = self.driver.find_element_by_xpath('//*[@id="topPagination"]/div/ul/li[3]/a[@title="Next"]')
        for num in range(0,deepth):
            # waiting for results to load
            #wait = WebDriverWait(self.driver, 2)
            #products = wait.until(EC.visibility_of_element_located((By.ID, "productsCatalog")))
            products = self.driver.find_elements_by_xpath("//*[@id='productsCatalog']/div")
            productDetailsPages = []
            ##for result in products.find_elements_by_class_name("b-catalogList__itmLink"):
            for result in products:
                #print("%%%result：",result)
                #print(result.get_attribute("innerHTML"))
                detailsPage = result.find_element_by_xpath("li/a").get_attribute("href")
                productDetailsPages.append(detailsPage)
            # print(productMainPages)
            self.getImageandSave(self.driver, productDetailsPages)
            #nextPage = self.driver.find_element_by_xpath('//*[@id="topPagination"]/div/ul/li[3]/a[@title="Next"]')
            #if nextPage is not None:
                #nextPage.click()
        print("\n@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n")
        self.driver.quit() 

save_path = "C:/Users/Administrator/Desktop/Buy_Dresses/"  # 爬取的照片存储主路径
startPage = 1  # 开始爬取的页面
deepth = 3  # 爬取的深度/页数
taobao = BuyDressesSpider(save_path)  # 获得taobaoMM_Spider实例
taobao.main(save_path, startPage, deepth)  # 调用main函数开始爬取
