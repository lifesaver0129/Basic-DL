# -*- coding: utf-8 -*-
'''
Created on 2016年10月31日

@author: Administrator
'''
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import os, time, queue, urllib
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
            try:
                crawlPageContent(data)
            except:
                print('page error')
        else:
            queueLock.release()
#         time.sleep(1)

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

#function count_web_elements is used to count web elements
def count_web_elements(driver, xpath):
    element = driver.find_elements_by_xpath(xpath)
    return len(element)


def check_exists_by_xpath(driver, xpath):
    try:
        if len(driver.find_element_by_xpath(xpath).text) > 1:
            return False 
    except NoSuchElementException:
        return False
    return True


def close_pop_window(driver):
    try:
        driver.find_element_by_xpath("//div[@class='eg-close-step-1 eg-invisibleButton']").click()
    except:
        print('Close pop window errror!')
    
    
def crawlPageContent(page_url):
    driver = webdriver.PhantomJS()
#     driver = webdriver.Firefox()
    driver.get(page_url)
    #下面是要爬取的pruductPage具体内容
    product_sku = driver.find_element_by_xpath("//td[@itemprop='sku']").text
#     print("product_sku:", product_sku)

    #下面是要爬取的pruductPage具体内容
    #建立存图片的文件夹路径 category层级
    product_breadcrumbs = ''
    try:
        ele_product_breadcrumbs = driver.find_elements_by_xpath('//ul[@class="b-breadcrumbs"]/li')
        for path_element in ele_product_breadcrumbs:
            product_breadcrumbs = product_breadcrumbs + path_element.text + '/'
    except:
        product_breadcrumbs = 'Home/Unclassified/'
#     print("product_breadcrumbs:", product_breadcrumbs)
    
    #product_path product 所在的目录
    product_path = 'C:/Users/Administrator/Desktop/' + product_breadcrumbs + str(product_sku) + '/'
#     print("product_path:", product_breadcrumbs + str(product_sku))
    
    #store in folder
    if not os.path.exists(product_path):  ###判断文件是否存在，返回布尔值
        os.makedirs(product_path)

    #产品来源网站 product_website
    product_website= 'www.zalora.com.hk'
#     print("product_website:", product_website)
    
    #product gender 默认Women 是0
    product_gender = product_breadcrumbs.split('/')[1]
    if str(product_gender) == 'Women':
        product_gender = 0
    else:
        product_gender = 1
#     print("product_gender:", product_gender)

    #product__brand 产品品牌
    product__brand = ''
    try:
        product__brand = driver.find_element_by_xpath("//div[@class='js-prd-brand product__brand']/a").text
    except:
        print("product__brand error")

    #product_craw_time 爬取产品时间
    product_craw_time = time.strftime(ISOTIMEFORMAT,time.localtime(time.time())) #获取当前时区时间格式 2016-08-02 21:46:38
#     print("product_craw_time:", product_craw_time)

    #product_update_time 更新产品时间 第一次爬取时，默认是product_craw_time
    product_update_time = time.strftime(ISOTIMEFORMAT,time.localtime(time.time())) #获取当前时区时间格式 2016-08-02 21:46:38
#     print("product_update_time:", product_update_time)

    #product__title 产品名
    product__title = ''
    try:
        product__title = driver.find_element_by_xpath("//div[@class='product__title fsm']").text
    except:
        print("product__title error")

    #product_price_box 产品价格,包括old_price 和price
    product_price_box = 1
    try:
        product_price_box = count_web_elements(driver, "//div[@class='price-box lfloat']/div")
    except:
        print('product_price_box error')
    #there is special price
    if product_price_box == 2:
        try:
            product_old_price = driver.find_element_by_xpath("//div[@class='price-box__old-price']").text
#             print("product_old_price:", product_old_price)
        except NoSuchElementException as e:
            product_old_price = ''
#             print("product_old_price:", product_old_price)
        #product_price 产品价格
        try:
            product_price = driver.find_element_by_xpath("//div[@class='price-box__special-price']").text
#             print("product_price:", product_price)
        except NoSuchElementException as e:
            product_price = ''
#             print("product_price:", product_price)
    #no special price
    if product_price_box == 1:
        #product_price 产品价格
        try:
            product_price = driver.find_element_by_xpath("//div[@class='price-box__regular-price']").text
#             print("product_price:", product_price)
        except NoSuchElementException as e:
            product_price = ''
#             print("product_price:", product_price)
        product_old_price = ''
    #productDesc 产品描述
    productDesc = ''
    try:
        productDesc = driver.find_element_by_xpath("//div[@id='productDesc']").text
#         print("productDesc:", productDesc)
    except:
        print("productDesc error")

    #product_option_stock_hint 产品库存信息
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
                driver.execute_script('$(arguments[0]).click()', ele_size_system)
                #ele_size_system.click()
                prdSizeOption = driver.find_element_by_xpath('//select[@class="js-subSelect prdSizeOption__sizeDetail "]')
                for ele_prdSizeOption in prdSizeOption.find_elements_by_tag_name('option'):
                    #check if the option is clickable
                    if ele_prdSizeOption.is_enabled():
                        driver.execute_script('$(arguments[0]).click()', ele_prdSizeOption)
                        #ele_prdSizeOption.click()
                        #print(ele_prdSizeOption.text)
                        user_selection = driver.find_element_by_xpath('//span[@id="product-option-stock-number"]')
                        product_stock = product_stock + ele_size_system.text + ':' + ele_prdSizeOption.text + ',' + user_selection.text + ';'
                        #print(user_selection.text)
#         print("product_stock:", product_stock)
    if num_select == 1:
        for ele_size_system in driver.find_elements_by_xpath('//div[@class="prd-option-collection prdSizeOption box size"]/select/option'):
            #check if the option is clickable
            if ele_size_system.is_enabled():
                #ele_size_system.click()
                driver.execute_script('$(arguments[0]).click()', ele_size_system)
                user_selection = driver.find_element_by_xpath('//span[@id="product-option-stock-number"]')
                product_stock = product_stock + ele_size_system.text + ':' + user_selection.text + ';'
#         print("product_stock:", product_stock)
    if num_select == 0:
        size_system = driver.find_element_by_xpath('//div[@class="prd-option-collection prdSizeOption box size"]')
        product_stock = product_stock + size_system.text + ';'
        product_option_stock_hint = driver.find_element_by_xpath('//span[@id="product-option-stock-number"]')
        product_stock = product_stock + product_option_stock_hint.text
#         print("product_stock:", product_stock)
    
    #product_usp_box是以下四个参数的父 element
    product_usp_box = driver.find_element_by_xpath(("//ul[@class='product__usp box mtl']"))
    product_usp_box_content = str(product_usp_box.text)
    #product_delivery_free_above 快递信息
    product_delivery = ''
    if "Free Delivery" in product_usp_box_content:
        product_delivery_free_above = driver.find_elements_by_xpath("//a[@id='cms-usp__cod']/span")
        for ele_product_delivery_free_above in product_delivery_free_above:
            product_delivery = product_delivery + ':' + ele_product_delivery_free_above.text
#         print("product_delivery_free_above", product_delivery)

    #product_cash_on_delivery 货到付款规则
    product_cash_on_delivery = ''
    if "Cash On Delivery" in product_usp_box_content:
        product_cash_on_delivery = 'Yes'
#         print("product_cash_on_delivery", product_cash_on_delivery)

    #returnPolicy 退货规则 product_free_30days_return
    returnPolicy = ''
    if "Return" in product_usp_box_content:
        product_free_30days_return = driver.find_elements_by_xpath("//a[@id='cms-freeReturn']/span")
        for ele_product_free_30days_return in product_free_30days_return:
            returnPolicy = returnPolicy + ':' + ele_product_free_30days_return.text
#         print("product_free_30days_return", returnPolicy)

    #product_estimated_delivery_time 估计运到时间
    product_estimated_delivery_time = driver.find_element_by_xpath("//i[@id='estimated_delivery_time']").text
#     print("product_estimated_delivery_time:", product_estimated_delivery_time)
    
    #product__details 产品详细
    try:
        product_details_table = driver.find_element_by_xpath("//div[@id='productDetails']/table/tbody")
        all_rows = product_details_table.find_elements_by_tag_name("tr")
        attribute_length = 0
        product_details_txt = ''
        for row in all_rows:
            cells = row.find_elements_by_tag_name("td")
            product_details_txt = product_details_txt + cells[0].text
            product_details_txt = product_details_txt + '%'
            product_details_txt = product_details_txt + cells[1].text
            product_details_txt = product_details_txt + '||'
            attribute_length = attribute_length + 1
        product_details_txt =  str(attribute_length) + '#' + product_details_txt
#         print("product_details_txt:", product_details_txt)
    except NoSuchElementException as e:
        product_details_txt = ''
#         print("product_details_txt:", product_details_txt)

    #product__size_details_tab1 size 详细
    try:
        sizeDetailTab_link = driver.find_element_by_xpath("//li[@class='sizeDetailTab']/a")
        #sizeDetailTab_link.click()
        driver.execute_script('$(arguments[0]).click()', sizeDetailTab_link)
        product__size_details_tab1 = driver.find_element_by_xpath("//div[@class='size__measurement unit size1of3 box']").text
#         print("product__size_details_tab1:", product__size_details_tab1)
    except NoSuchElementException as e:
        product__size_details_tab1 = ''
#         print("product__size_details_tab1:", product__size_details_tab1)

    #product__size_details_tab2 model 详细
    try:
        product__size_details_tab2 = driver.find_element_by_xpath("//div[@class='size__attributes unit size1of3 box']").text
#         print("product__size_details_tab2:", product__size_details_tab2)
    except NoSuchElementException as e:
        product__size_details_tab2 = ''
#         print("product__size_details_tab2:", product__size_details_tab2)

    #product__size_details_tab3 size 详细
    try:
        product__size_details_tab3 = driver.find_element_by_xpath("//div[@class='size__helper unit size1of3 box']").text
#         print("product__size_details_tab3:", product__size_details_tab3)
    except NoSuchElementException as e:
        product__size_details_tab3 = ''
#         print("product__size_details_tab3:", product__size_details_tab3)

    #IMG number of the product
    try:
        img_url_list = []
        img_number = 0
        ele_imgs = driver.find_elements_by_xpath('//ul[@class="prd-moreImagesList ui-listItemBorder ui-listLight swiper-wrapper"]/li')
        for ele in ele_imgs:
            img_url_list.append(ele.get_attribute("data-image-big"))
        img_url_list = list(set(img_url_list))
        img_number = saveImgs(driver, product_path, img_url_list)
    except:
        print('IMG error')
#     print("img_number:", img_number)

    #product_img_path product IMG folder path
    product_img_path = product_breadcrumbs + str(product_sku)
#     print("product_img_path:", product_img_path)

    #product_reviews 产品评论
    product_reviews = ''
#     print("product_reviews:", product_reviews)
    
    product_details_data = (product_breadcrumbs, product_sku, product_website, 
                            product_gender, product__brand, product_craw_time, product_update_time, 
                            product__title, product_old_price, product_price, productDesc, product_stock, 
                            product_delivery, product_cash_on_delivery, returnPolicy, product_estimated_delivery_time, 
                            product_details_txt, product__size_details_tab1, product__size_details_tab2, product__size_details_tab3, 
                            img_number, product_img_path, product_reviews)
    
    databse_list = ''
    for i in range(0,23):
        databse_list = databse_list + str(product_details_data[i]).replace('\n', '') + '||'
    databse_list = databse_list.strip('*')
    with open('C:/Users/Administrator/Desktop/zalora_database.txt','a', encoding="utf8") as f:
        f.write(databse_list + '\n')
    driver.quit()


# start of main function ****************************************************
category_file = open("C:/Users/Administrator/Desktop/zalora_URLs.txt")
 
lines = category_file.readlines()
category_file.close()
     
threadList = ["Thread-1", "Thread-2", "Thread-3", "Thread-4", "Thread-5", "Thread-6", "Thread-7", "Thread-8", "Thread-9", "Thread-10" \
              "Thread-11", "Thread-12", "Thread-13", "Thread-14", "Thread-15", "Thread-16", "Thread-17", "Thread-18", "Thread-19", "Thread-20"]
# threadList = ["Thread-1", "Thread-2", "Thread-3", "Thread-4", "Thread-5", "Thread-6", "Thread-7", "Thread-8"]
# threadList = ["Thread-1", "Thread-2", "Thread-3", "Thread-4"]
nameList = lines
queueLock = threading.Lock()
workQueue = queue.Queue(len(nameList) + len(threadList))
threads = []
threadID = 1
 
# 创建新线程
for tName in range(len(threadList)):
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


# driver = webdriver.Firefox()
# driver.get('https://www.zalora.com.hk/sunnydaysweety-new-style-embroidered-knitted-jacket-ca10131be-4673457.html')