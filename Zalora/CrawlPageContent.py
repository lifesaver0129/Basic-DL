'''
Created on 2016年7月10日
@author: Administrator
'''
import re
import time
import requests
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException    
import csv,os
ISOTIMEFORMAT='%Y-%m-%d %X'    #Time setup


def readURL(path):
    #写入csv文件 文件名
    LIST = []
    f = open(path+'listURL.csv')
    reader = csv.reader(f)
    for line in reader:
        LIST.append(line[0])
    return LIST
    f.close()

#crawl IMGs
def saveImgs(img_path):
    img_list = driver.find_elements_by_xpath('//ul[@class="prd-moreImagesList ui-listItemBorder ui-listLight swiper-wrapper"]/li')
    img_url_list = []
    for imageElement in img_list:
        image_url = imageElement.get_attribute("data-image-big")
        img_url_list.append(image_url)
    try:
        if img_url_list[0] == img_url_list[1]:
            del img_url_list[0]
    except:
        print('Only one IMG!!')
    img_num = 0
    while img_num < len(img_url_list):
        image_url = img_url_list[img_num]
        if not os.path.exists(img_path):  ###判断文件是否存在，返回布尔值
            os.makedirs(img_path)
        img_postfix = re.search(r'(\.jpg|\.png)$', str(image_url))
        save_path = img_path + '/' + str(img_num + 1) + str(img_postfix.group())
        r = requests.get(image_url, stream=True)
        with open(save_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:  # filter out keep-alive new chunks
                    f.write(chunk)
                    f.flush()
        img_num = img_num + 1
        f.close()
    return img_num

#Crawl product contents
def crawlContents(URL):
    #建立存图片的文件夹路径 category层级
    path_element = driver.find_elements_by_xpath('//ul[@class="b-breadcrumbs"]/li')
    product_breadcrumbs = ''
    for path_element_content in path_element:
        product_breadcrumbs = product_breadcrumbs + path_element_content.text + '/'
    
    #下面是要爬取的pruductPage具体内容
    product_sku = driver.find_element_by_xpath("//td[@itemprop='sku']").text
    print(product_sku)
    product_path = path + product_breadcrumbs + str(product_sku)
    #store in folder
    if not os.path.exists(product_path):  ###判断文件是否存在，返回布尔值
        os.makedirs(product_path)

    #写入txt文件
    detailsFileName = product_path + '/' + str(product_sku) + ".txt"
    f = open(detailsFileName, "w+", encoding='utf-8')
    
    #存图片的文件夹路径 category层级
    f.write('product_breadcrumbsstr:' + str(product_breadcrumbs)+'\n')
    
    #产品来源网站 product_website
    f.write('product_website:' + 'www.zalora.com.hk' +'\n')
    
    #product gender 默认是Women
    try:
        product_gender = product_breadcrumbs.split('/')[1]
        f.write('product gender:' + str(product_gender) +'\n')
    except:
        f.write('product gender:' + 'Women' +'\n')
        
    #product__brand 产品品牌
    try:
        product__brand = driver.find_element_by_xpath("//div[@class='js-prd-brand product__brand']/a").text
        f.write('product__brand:' + str(product__brand)+'\n')
    except NoSuchElementException as e:
        product__brand = 'NULL'
        f.write('product__brand NOT EXISTS:' + str(product__brand)+'\n')

    #product_craw_time 爬取产品时间
    product_craw_time = time.strftime(ISOTIMEFORMAT,time.localtime(time.time())) #获取当前时区时间格式 2016-08-02 21:46:38
    try:
        f.write('product_craw_time:' + str(product_craw_time)+'\n')
    except:
        product_craw_time = 'NULL'
        f.write('product_craw_time NOT EXISTS:' + str(product_craw_time)+'\n')

    #product_update_time 更新产品时间 第一次爬取时，默认是product_craw_time
    try:
        f.write('product_update_time:' + str(product_craw_time)+'\n')
    except:
        product_craw_time = 'NULL'
        f.write('product_update_time NOT EXISTS:' + str(product_craw_time)+'\n')

    #product_SKU 产品SKU code
    try:
        f.write('product_sku:' + str(product_sku)+'\n')
    except:
        product_sku = 'NULL'
        f.write('product_sku NOT EXISTS:' + str(product_sku)+'\n')

    #product_URL 产品URL code
    try:
        f.write('product_URL:' + str(URL)+'\n')
    except:
        product_URL = 'NULL'
        f.write('product_URL NOT EXISTS:' + str(product_URL)+'\n')

    #product__title 产品名
    try:
        product__title = driver.find_element_by_xpath("//div[@class='product__title fsm']").text
        f.write('product__title:' + str(product__title)+'\n')
    except NoSuchElementException as e:
        product__title = 'NULL'
        f.write('product__title NOT EXISTS:' + str(product__title)+'\n')

    #product_old_price 产品价格
    try:
        product_old_price = driver.find_element_by_xpath("//div[@class='price-box__old-price']").text
        f.write('product_old_price:' + str(product_old_price)+'\n')
    except NoSuchElementException as e:
        product_old_price = 'NULL'
        f.write('product_old_price NOT EXISTS:' + str(product_old_price)+'\n')

    #product_price 产品价格
    try:
        product_price = driver.find_element_by_xpath("//div[@class='price-box lfloat']").text
        f.write('product_price:' + str(product_price)+'\n')
    except NoSuchElementException as e:
        product_price = 'NULL'
        f.write('product_price NOT EXISTS:' + str(product_price)+'\n')
        
    #productDesc 产品描述
    try:
        productDesc = driver.find_element_by_xpath("//div[@id='productDesc']").text
        f.write('productDesc:' + str(productDesc)+'\n')
    except NoSuchElementException as e:
        productDesc = 'NULL'
        f.write('productDesc NOT EXISTS:' + str(productDesc)+'\n')

        
    #product_option_stock_hint 产品库存信息
    try:
        product_option_stock_hint = driver.find_element_by_xpath("//div[@class='mtm usr-selection']").text
        f.write('product_option_stock_hint:' + str(product_option_stock_hint)+'\n')
    except NoSuchElementException as e:
        product_option_stock_hint = 'NULL'
        f.write('product_option_stock_hint NOT EXISTS:' + str(product_option_stock_hint)+'\n')
    
    #product_delivery_free_above 快递信息
    try:
        product_delivery_free_above = driver.find_element_by_xpath("//ul[@class='product__usp box mtl']/li[1]/a/span[2]").text
        f.write('product_delivery_free_above:' + str(product_delivery_free_above)+'\n')
    except NoSuchElementException as e:
        product_delivery_free_above = 'No'
        f.write('product_delivery_free_above NOT EXISTS:' + str(product_delivery_free_above)+'\n')
    
    #returnPolicy 退货规则
    try:
        product_free_30days_return = driver.find_element_by_xpath("//ul[@class='product__usp box mtl']/li[2]/a/span[2]").text
        f.write('product_free_30days_return:' + str(product_free_30days_return)+'\n')
    except NoSuchElementException as e:
        product_free_30days_return = 'No'
        f.write('product_free_30days_return NOT EXISTS:' + str(product_free_30days_return)+'\n')
    
    #product_cash_on_delivery 货到付款
    try:
        product_cash_on_delivery = driver.find_element_by_xpath("//ul[@class='product__usp box mtl']/li[3]/span[2]").text
        f.write('product_cash_on_delivery:' + str(product_cash_on_delivery)+'\n')
    except NoSuchElementException as e:
        product_cash_on_delivery = 'No'
        f.write('product_cash_on_delivery NOT EXISTS:' + str(product_cash_on_delivery)+'\n')
    
    #product_estimated_delivery_time 估计运到时间
    try:
        product_estimated_delivery_time = driver.find_element_by_xpath("//i[@id='estimated_delivery_time']").text
        f.write('product_estimated_delivery_time:' + str(product_estimated_delivery_time)+'\n')
    except NoSuchElementException as e:
        product_estimated_delivery_time = 'NULL'
        f.write('product_estimated_delivery_time  NOT EXISTS:' + str(product_estimated_delivery_time)+'\n')
        
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
        f.write('productDetails:' + str(product_details_txt)+'\n')
    except NoSuchElementException as e:
        product_details_txt = 'NULL'
        f.write('productDetails NOT EXISTS:' + str(product_details_txt)+'\n')

    #product__size_details_tab1 size 详细
    try:
        sizeDetailTab_link = driver.find_element_by_xpath("//li[@class='sizeDetailTab']/a")
        sizeDetailTab_link.click()
        product__size_details_tab1 = driver.find_element_by_xpath("//div[@class='size__measurement unit size1of3 box']").text
        f.write('product__size_details_tab1:' + str(product__size_details_tab1)+'\n')
    except NoSuchElementException as e:
        product__size_details_tab1 = 'NULL'
        f.write('product__size_details NOT EXISTS:' + str(product__size_details_tab1)+'\n')

    #product__size_details_tab2 model 详细
    try:
        product__size_details_tab2 = driver.find_element_by_xpath("//div[@class='size__attributes unit size1of3 box']").text
        f.write('product__size_details_tab2:' + str(product__size_details_tab2)+'\n')
    except NoSuchElementException as e:
        product__size_details_tab2 = 'NULL'
        f.write('product__size_details_tab2 NOT EXISTS:' + str(product__size_details_tab2)+'\n')

    #product__size_details_tab3 size 详细
    try:
        product__size_details_tab3 = driver.find_element_by_xpath("//div[@class='size__helper unit size1of3 box']").text
        f.write('product__size_details_tab3:' + str(product__size_details_tab3)+'\n')
    except NoSuchElementException as e:
        product__size_details_tab3 = 'NULL'
        f.write('product__size_details_tab3 NOT EXISTS:' + str(product__size_details_tab3)+'\n')

    #IMG number of the product
    img_number = saveImgs(product_path)
    f.write('img_number:' + str(img_number)+'\n')    

    #product_img_path product IMG folder path
    try:
        product_img_path = product_breadcrumbs + str(product_sku)
        f.write('product_img_path path:' + str(product_img_path)+'\n')
    except NoSuchElementException as e:
        product_img_path = 'NULL'
        f.write('product_img_path path:' + str(product_img_path)+'\n')

    #product_reviews 产品评论
    try:
        product_reviews = ''
        f.write('product_reviews:' + str(product_reviews)+'\n')
    except NoSuchElementException as e:
        product_reviews = 'NULL'
        f.write('product_reviews:' + str(product_reviews)+'\n')

    
    #close the file stream
    f.close()
    driver.close()

path = 'C:/Users/Administrator/Desktop/'
#nextPage = self.driver.find_element_by_xpath('//*[@id="topPagination"]/div/ul/li[3]/a[@title="Next"]')
content_list = []
listURL = readURL(path)

n = 0
while n<len(listURL):
    print(n)
    product_URL = listURL[n]
    driver = webdriver.Firefox()
    try:
        driver.get(product_URL)
    except NoSuchElementException as e:
        print('Page not found')
    #关闭跳出窗口
        
    modal = driver.find_element_by_xpath('//div[@class="eg-close-step-1 eg-invisibleButton"]')
    if modal is not None:
        modal.click()
    else:
        print('Page not found')
    
    #尝试抓取product内容，存在已经撤销的链接，网站直接转到page not found页面
    try:
        crawlContents(product_URL)
    except NoSuchElementException as e:
        #page_not_found = driver.find_element_by_xpath('//div[@class="b-notfound__header txtUpper"]')
        print('WARNING: PAGE NOT FOUND')
        driver.close()
    #爬取下一个链接
    n = n + 1
quit()