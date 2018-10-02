'''
Created on 2016年9月23日
Crawling page content in H&M
@author: Administrator
'''

import os, time, queue, urllib
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException    
import threading
ISOTIMEFORMAT='%Y-%m-%d %X'    #Time setup


exitFlag = 0

class myThread (threading.Thread):
    def __init__(self, threadID, name, q):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.q = q
    def run(self):
#         print ("开启线程：" + self.name)
        process_data(self.name, self.q)
#         print ("退出线程：" + self.name)

def process_data(threadName, q):
    while not exitFlag:
        queueLock.acquire()
        if not workQueue.empty():
            data = q.get()
            queueLock.release()
            print ("%s processing %s" % (threadName, data))
            crawl_page_contents(data)
        else:
            queueLock.release()
        time.sleep(1)

def check_exists_by_xpath(driver, xpath):
    try:
        driver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False
    return True


#crawl IMGs
def saveImgs(driver, img_path, img_url_list):
    img_num = 0
    if not os.path.exists(img_path):  ###判断文件是否存在，返回布尔值
        os.makedirs(img_path)
    
    while img_num < len(img_url_list):
        image_url = img_url_list[img_num]
        save_path = img_path + str(img_num) + '.jpg'
        urllib.request.urlretrieve(image_url, save_path)
        img_num = img_num + 1
    return img_num

def crawl_page_contents(page_url):
    prodocut_id = page_url.split("=")[1].strip('\n') + "/"
    #driver = webdriver.Firefox()
    driver = webdriver.PhantomJS()
    driver.get(page_url)
    #The breadcrumbs **************************************************************
    ele_breadcrumbs = driver.find_elements_by_xpath("//ul[@class='breadcrumbs']/li/a")
    breadcrumbs = ''
    for ele_breadcrumb in ele_breadcrumbs:
        breadcrumbs = breadcrumbs + str(ele_breadcrumb.text).strip() + '/'
    breadcrumbs = breadcrumbs.replace(" /", "/")
#     print('Breadcrumbs:', breadcrumbs)
    #End of breadcrumbs **************************************************************
    
    
    #The product title and price **************************************************************
    ele_title = str(driver.find_element_by_xpath("//form[@id='product']/h1").text)
    title = ele_title.split('\n')[0]
    price = ele_title.split('\n')[1]
#     print('Title:', title)
#     print('Price:', price)
    #End of product title **************************************************************
    
    
    #The product details **************************************************************
    ele_details = driver.find_element_by_xpath("//div[@class='details']")
    #including colour, size details and dilivery info.
    colour = []
    if check_exists_by_xpath(driver, "//ul[@class='options articles clearfix']/li/a/span"):
        ele_colour = ele_details.find_elements_by_xpath("//ul[@class='options articles clearfix']/li/a/span")
        for ele in ele_colour:
            if ele.text != '':
                colour.append(ele.text)
#         print('Colour:', colour)
    
    if check_exists_by_xpath(driver, "//span[@id='text-selected-variant']"):
        size = ele_details.find_element_by_xpath("//span[@id='text-selected-variant']").text
    else:
        size = ''
#     print('Size:', size)
    
    dilivery = ''
    if check_exists_by_xpath(ele_details, "//p[2]"):
        dilivery = ele_details.find_element_by_xpath("//p[2]").text
#         print('Dilivery:', dilivery)
    #End of size available **************************************************************
    
    #The product description **************************************************************
    description = ''
    if check_exists_by_xpath(driver, "//div[@class='description']/p[1]"):
        description = driver.find_element_by_xpath("//div[@class='description']/p[1]").text
    #including description and care instruction.
#     print('Description', description)
    
    care_instruction = ''
    if check_exists_by_xpath(driver, "//div[@class='description']/p[2]"):
        care_instruction = driver.find_element_by_xpath("//div[@class='description']/p[2]").text
#     print('Care Instruction:', care_instruction)
    #End of description **************************************************************
    
    #The product IMGs **************************************************************
    if check_exists_by_xpath(driver, "//ul[@id='product-thumbs']/li/a"):
        ele_imgs = driver.find_elements_by_xpath("//ul[@id='product-thumbs']/li/a")
        img_url_list = []
        for ele in ele_imgs:
            img_url_list.append(ele.get_attribute("href"))
        img_number = saveImgs(driver, ROOTPATH + prodocut_id, img_url_list)
#         print('Img number:', img_number)
    #End of product IMGs **************************************************************
    
    #The similar products **************************************************************
    if check_exists_by_xpath(driver, "//div[@class='scrollable area-container area-container-PRA9']/div/ul/li/div/a"):
        ele_style_with = driver.find_elements_by_xpath("//div[@class='scrollable area-container area-container-PRA9']/div/ul/li/div/a")
        style_with_list = []
        for ele in ele_style_with:
            style_with_list.append(ele.get_attribute("href"))
#         print('len(style_with_list)', len(style_with_list))
    if check_exists_by_xpath(driver, "//div[@class='area-container area-container-PRA1 scrollable-initiated']/div/ul/li/div/a"):
        ele_similar = driver.find_elements_by_xpath("//div[@class='area-container area-container-PRA1 scrollable-initiated']/div/ul/li/div/a")
        similar_list = []
        for ele in ele_similar:
            similar_list.append(ele.get_attribute("href"))
        
#         print('len(similar_list)', len(similar_list))
    #End of similar products **************************************************************
    driver.quit()

ROOTPATH = "C:/Users/Administrator/Desktop/H&M/"
file = open("C:/Users/Administrator/Desktop/H&M_ladies_urls.txt")
# url = 'http://www.hm.com/hk/en/product/54618?article=54618-B'
lines = file.readlines()
file.close()
    
threadList = ["Thread-1", "Thread-2", "Thread-3", "Thread-4", "Thread-5", "Thread-6", "Thread-7", "Thread-8", "Thread-9", "Thread-10"]
nameList = lines
queueLock = threading.Lock()
workQueue = queue.Queue(len(nameList) + 10)
threads = []
threadID = 1

# 创建新线程
for tName in range(10):
    thread = myThread(threadID, tName, workQueue)
    thread.start()
    threads.append(thread)
    threadID += 1

# 填充队列
queueLock.acquire()
for word in nameList:
    workQueue.put(word)
queueLock.release()

# 等待队列清空
while not workQueue.empty():
    pass

# 通知线程是时候退出
exitFlag = 1

# 等待所有线程完成
for t in threads:
    t.join()
print ("退出主线程")
