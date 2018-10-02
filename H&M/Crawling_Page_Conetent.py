'''
Created on 2016年9月27日
Crawling page content in H&M
Using single-threading

@author: Administrator
'''
import os, time, urllib, pymysql
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException    
ISOTIMEFORMAT='%Y-%m-%d %X'    #Time setup

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
    prodocut_id = page_url.split("=")[1].strip('\n')
    product_website = "http://www.hm.com/hk/en/"
    product_url = page_url
    product_gender = 1
    product__brand = "H&M"
    product_url_stat = 1
    
    #driver = webdriver.Firefox()
    driver = webdriver.PhantomJS()
    driver.get(page_url)
    #product_craw_time 爬取产品时间
    product_craw_time = time.strftime(ISOTIMEFORMAT,time.localtime(time.time())) #获取当前时区时间格式 2016-08-02 21:46:38
    
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
    product_title = ele_title.split('\n')[0]
    product_price = ele_title.split('\n')[1]
#     print('Title:', title)
#     print('Price:', price)
    #End of product title **************************************************************
    
    
    #The product details **************************************************************
    ele_details = driver.find_element_by_xpath("//div[@class='details']")
    #including colour, size details and dilivery info.
    colour = ""
    if check_exists_by_xpath(driver, "//ul[@class='options articles clearfix']/li/a/span"):
        ele_colour = ele_details.find_elements_by_xpath("//ul[@class='options articles clearfix']/li/a/span")
        for ele in ele_colour:
            if ele.text != '':
                colour = colour + ";"
#         print('Colour:', colour)
    
    if check_exists_by_xpath(driver, "//span[@id='text-selected-variant']"):
        product_stock_size = ele_details.find_element_by_xpath("//span[@id='text-selected-variant']").text
    else:
        product_stock_size = ''
#     print('Size:', size)
    
    if check_exists_by_xpath(ele_details, "//p[2]"):
        product_dilivery = ele_details.find_element_by_xpath("//p[2]").text
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
        img_number = saveImgs(driver, ROOTPATH + prodocut_id + "/", img_url_list)
#         print('Img number:', img_number)
    #End of product IMGs **************************************************************
    
    #The similar products **************************************************************
    if check_exists_by_xpath(driver, "//div[@class='scrollable area-container area-container-PRA9']/div/ul/li/div/a"):
        ele_style_with = driver.find_elements_by_xpath("//div[@class='scrollable area-container area-container-PRA9']/div/ul/li/div/a")
        style_with_list = ''
        for ele in ele_style_with:
            style_with_list = style_with_list + ele.get_attribute("href") + ";"
#         print('len(style_with_list)', len(style_with_list))
    if check_exists_by_xpath(driver, "//div[@class='area-container area-container-PRA1 scrollable-initiated']/div/ul/li/div/a"):
        ele_similar = driver.find_elements_by_xpath("//div[@class='area-container area-container-PRA1 scrollable-initiated']/div/ul/li/div/a")
        similar_list = ''
        for ele in ele_similar:
            similar_list = similar_list + ele.get_attribute("href") + ";"
#         print('len(similar_list)', len(similar_list))
    #End of similar products **************************************************************
    
    
    #start of database updating
    sql_update_content = """\
    INSERT INTO testdb.product(
    product_breadcrumbs,
    product_url,
    product_url_stat,
    product_sku,
    product_website,
    product_gender,
    product_brand,
    product_craw_time,
    product_title,
    product_estimated_delivery_time,
    product_price,
    product_desc,
    product_stock_hint,
    product_size_detail1,
    product_img_number,
    product_similar,
    product_match)
    VALUES
    (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""

    product_details_data = (breadcrumbs, product_url, product_url_stat, prodocut_id, product_website, 
                            product_gender, product__brand, product_craw_time, 
                            product_title, product_dilivery, product_price, description, product_stock_size,
                            care_instruction, img_number, similar_list.strip(";"), style_with_list.strip(";"))
    cursor.execute(sql_update_content, product_details_data)
    db.commit()#需要这一句才能保存到数据库中
    
    #end of database updating
    
    driver.quit()



def update_crawl_page_contents(page_url):
    #driver = webdriver.Firefox()
    driver = webdriver.PhantomJS()
    driver.get(page_url)
    product_sku = page_url.split("=")[1].strip('\n')
    #The similar products **************************************************************
    if check_exists_by_xpath(driver, "//div[@class='area-container area-container-PRA1 scrollable-initiated']/div/ul/li/div/a"):
        ele_similar = driver.find_elements_by_xpath("//div[@class='area-container area-container-PRA1 scrollable-initiated']/div/ul/li/div/a")
        global similar_list
        similar_list = ''
        for ele in ele_similar:
            similar_list = similar_list + ele.get_attribute("href").strip("\n") + ";"

    if check_exists_by_xpath(driver, "//div[@class='scrollable area-container area-container-PRA9']/div/ul/li/div/a"):
        ele_style_with = driver.find_elements_by_xpath("//div[@class='scrollable area-container area-container-PRA9']/div/ul/li/div/a")
        global style_with_list
        style_with_list = ''
        for ele in ele_style_with:
            style_with_list = style_with_list + ele.get_attribute("href") + ";"
    #End of similar products **************************************************************
    
    
    #start of database updating
    sql_update_content = """update testdb.product SET product_similar = %s, product_match = %s where product_sku = %s"""
    update_data = (similar_list, style_with_list, product_sku)
    cursor.execute(sql_update_content, update_data)
    db.commit()#需要这一句才能保存到数据库中
    
    #end of database updating
    driver.quit()
    
#begin the main function
#connect the database.
db = pymysql.connect("localhost","root","123456","testdb", charset="utf8")
# 使用cursor()方法获取操作游标 
cursor = db.cursor()

ROOTPATH = "C:/Users/Administrator/Desktop/H&M/"
file = open("C:/Users/Administrator/Desktop/H&M_ladies_urls.txt")
lines = file.readlines()
file.close()


# url = 'http://www.hm.com/hk/en/product/47714?article=47714-B'
# update_crawl_page_contents(url)
for line in lines:
    try:
        update_crawl_page_contents(line)
        print(line.split("=")[1].strip('\n'))
    except:
        print("ERROR!!!!!!!!!!")
        print(line)

db.close()