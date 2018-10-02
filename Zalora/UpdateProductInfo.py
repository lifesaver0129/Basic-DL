'''
Created on 2016年8月9日

@author: Administrator
'''
import requests,re,time,os,gc,pymysql
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
ISOTIMEFORMAT='%Y-%m-%d %X'    #Time setup

#function count_web_elements is used to count web elements
def count_web_elements(driver,id):
    number = 0
    element = driver.find_elements_by_xpath(id)
    for ele in element:
        number = number + 1
    return number

# update product information
def update_product_info(dbconn, statment, data):
    dbconn.execute(statment, data)
    dbconn.commit()#需要这一句才能保存到数据库中

#crawl IMGs return IMG number
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
#***********************************************************************************

def crawlPageContent(driver):
    #下面是要爬取的pruductPage具体内容
    product_sku = driver.find_element_by_xpath("//td[@itemprop='sku']").text
    print("product_sku:", product_sku)

    #建立存图片的文件夹路径 category层级
    path_elements = driver.find_elements_by_xpath('//ul[@class="b-breadcrumbs"]/li')
    #下面是要爬取的pruductPage具体内容
    product_breadcrumbs = ''
    if count_web_elements(driver, '//ul[@class="b-breadcrumbs"]/li') == 0:
        product_breadcrumbs = 'Home/Unclassified/'
    else:
        for path_element in path_elements:
            product_breadcrumbs = product_breadcrumbs + path_element.text + '/'
    print("product_breadcrumbs:", product_breadcrumbs)
    
    #product_path product 所在的目录
    product_path = 'C:/Users/Administrator/Desktop/' + product_breadcrumbs + str(product_sku)
    print("product_path:", product_breadcrumbs + str(product_sku))
    
    #store in folder
    if not os.path.exists(product_path):  ###判断文件是否存在，返回布尔值
        os.makedirs(product_path)

    #产品来源网站 product_website
    product_website= 'www.zalora.com.hk'
    print("product_website:", product_website)
    
    #product gender 默认Women 是0
    product_gender = product_breadcrumbs.split('/')[1]
    if str(product_gender) == 'Women':
        product_gender = 0
    else:
        product_gender = 1
    print("product_gender:", product_gender)

    #product__brand 产品品牌
    product__brand = driver.find_element_by_xpath("//div[@class='js-prd-brand product__brand']/a").text
    print("product__brand:", product__brand)

    #product_craw_time 爬取产品时间
    product_craw_time = time.strftime(ISOTIMEFORMAT,time.localtime(time.time())) #获取当前时区时间格式 2016-08-02 21:46:38
    print("product_craw_time:", product_craw_time)

    #product_update_time 更新产品时间 第一次爬取时，默认是product_craw_time
    product_update_time = time.strftime(ISOTIMEFORMAT,time.localtime(time.time())) #获取当前时区时间格式 2016-08-02 21:46:38
    print("product_update_time:", product_update_time)

    #product__title 产品名
    product__title = driver.find_element_by_xpath("//div[@class='product__title fsm']").text
    print("product__title:", product__title)

    #product_price_box 产品价格,包括old_price 和price
    product_price_box = count_web_elements(driver, "//div[@class='price-box lfloat']/div")
    #there is special price
    if product_price_box == 2:
        try:
            product_old_price = driver.find_element_by_xpath("//div[@class='price-box__old-price']").text
            print("product_old_price:", product_old_price)
        except NoSuchElementException as e:
            product_old_price = ''
            print("product_old_price:", product_old_price)
        #product_price 产品价格
        try:
            product_price = driver.find_element_by_xpath("//div[@class='price-box__special-price']").text
            print("product_price:", product_price)
        except NoSuchElementException as e:
            product_price = ''
            print("product_price:", product_price)
    #no special price
    if product_price_box == 1:
        #product_price 产品价格
        try:
            product_price = driver.find_element_by_xpath("//div[@class='price-box__regular-price']").text
            print("product_price:", product_price)
        except NoSuchElementException as e:
            product_price = ''
            print("product_price:", product_price)
        product_old_price = ''
    #productDesc 产品描述
    try:
        productDesc = driver.find_element_by_xpath("//div[@id='productDesc']").text
        print("productDesc:", productDesc)
    except NoSuchElementException as e:
        productDesc = ''
        print("productDesc:", productDesc)

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
        print("product_stock:", product_stock)
    if num_select == 1:
        for ele_size_system in driver.find_elements_by_xpath('//div[@class="prd-option-collection prdSizeOption box size"]/select/option'):
            #check if the option is clickable
            if ele_size_system.is_enabled():
                #ele_size_system.click()
                driver.execute_script('$(arguments[0]).click()', ele_size_system)
                user_selection = driver.find_element_by_xpath('//span[@id="product-option-stock-number"]')
                product_stock = product_stock + ele_size_system.text + ':' + user_selection.text + ';'
        print("product_stock:", product_stock)
    if num_select == 0:
        size_system = driver.find_element_by_xpath('//div[@class="prd-option-collection prdSizeOption box size"]')
        product_stock = product_stock + size_system.text + ';'
        product_option_stock_hint = driver.find_element_by_xpath('//span[@id="product-option-stock-number"]')
        product_stock = product_stock + product_option_stock_hint.text
        print("product_stock:", product_stock)
    
    #product_usp_box是以下四个参数的父 element
    product_usp_box = driver.find_element_by_xpath(("//ul[@class='product__usp box mtl']"))
    product_usp_box_content = str(product_usp_box.text)
    #product_delivery_free_above 快递信息
    product_delivery = ''
    if "Free Delivery" in product_usp_box_content:
        product_delivery_free_above = driver.find_elements_by_xpath("//a[@id='cms-usp__cod']/span")
        for ele_product_delivery_free_above in product_delivery_free_above:
            product_delivery = product_delivery + ':' + ele_product_delivery_free_above.text
        print("product_delivery_free_above", product_delivery)

    #product_cash_on_delivery 货到付款规则
    product_cash_on_delivery = ''
    if "Cash On Delivery" in product_usp_box_content:
        product_cash_on_delivery = 'Yes'
        print("product_cash_on_delivery", product_cash_on_delivery)

    #returnPolicy 退货规则 product_free_30days_return
    returnPolicy = ''
    if "Return" in product_usp_box_content:
        product_free_30days_return = driver.find_elements_by_xpath("//a[@id='cms-freeReturn']/span")
        for ele_product_free_30days_return in product_free_30days_return:
            returnPolicy = returnPolicy + ':' + ele_product_free_30days_return.text
        print("product_free_30days_return", returnPolicy)

    #product_estimated_delivery_time 估计运到时间
    product_estimated_delivery_time = driver.find_element_by_xpath("//i[@id='estimated_delivery_time']").text
    print("product_estimated_delivery_time:", product_estimated_delivery_time)
    
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
        print("product_details_txt:", product_details_txt)
    except NoSuchElementException as e:
        product_details_txt = ''
        print("product_details_txt:", product_details_txt)

    #product__size_details_tab1 size 详细
    try:
        sizeDetailTab_link = driver.find_element_by_xpath("//li[@class='sizeDetailTab']/a")
        #sizeDetailTab_link.click()
        driver.execute_script('$(arguments[0]).click()', sizeDetailTab_link)
        product__size_details_tab1 = driver.find_element_by_xpath("//div[@class='size__measurement unit size1of3 box']").text
        print("product__size_details_tab1:", product__size_details_tab1)
    except NoSuchElementException as e:
        product__size_details_tab1 = ''
        print("product__size_details_tab1:", product__size_details_tab1)

    #product__size_details_tab2 model 详细
    try:
        product__size_details_tab2 = driver.find_element_by_xpath("//div[@class='size__attributes unit size1of3 box']").text
        print("product__size_details_tab2:", product__size_details_tab2)
    except NoSuchElementException as e:
        product__size_details_tab2 = ''
        print("product__size_details_tab2:", product__size_details_tab2)

    #product__size_details_tab3 size 详细
    try:
        product__size_details_tab3 = driver.find_element_by_xpath("//div[@class='size__helper unit size1of3 box']").text
        print("product__size_details_tab3:", product__size_details_tab3)
    except NoSuchElementException as e:
        product__size_details_tab3 = ''
        print("product__size_details_tab3:", product__size_details_tab3)

    #IMG number of the product
    img_number = saveImgs(product_path)
    print("img_number:", img_number)

    #product_img_path product IMG folder path
    product_img_path = product_breadcrumbs + str(product_sku)
    print("product_img_path:", product_img_path)

    #product_reviews 产品评论
    product_reviews = ''
    print("product_reviews:", product_reviews)

    sql_update_content = """\
    UPDATE testdb.product SET
    product_breadcrumbs = %s,
    product_sku = %s,
    product_website = %s,
    product_gender = %s,
    product_brand = %s,
    product_craw_time = %s,
    product_update_time = %s,
    product_title = %s,
    product_price_old = %s,
    product_price = %s,
    product_desc = %s,
    product_stock_hint = %s,
    product_delivery_free_above = %s,
    product_cash_on_delivery = %s,
    product_free_30days_return = %s,
    product_estimated_delivery_time = %s,
    product_details = %s,
    product_size_detail1 = %s,
    product_size_detail2 = %s,
    product_size_detail3 = %s,
    product_img_number = %s,
    product_img_path = %s,
    product_review = %s where idproduct = %s"""

    product_details_data = (product_breadcrumbs, product_sku, product_website, 
                            product_gender, product__brand, product_craw_time, product_update_time, 
                            product__title, product_old_price, product_price, productDesc, product_stock, 
                            product_delivery, product_cash_on_delivery, returnPolicy, product_estimated_delivery_time, 
                            product_details_txt, product__size_details_tab1, product__size_details_tab2, product__size_details_tab3, 
                            img_number, product_img_path, product_reviews, start_number_one)
    cursor.execute(sql_update_content, product_details_data)
    db.commit()#需要这一句才能保存到数据库中

#begin the main function
#connect the database.
db = pymysql.connect("localhost","root","123456","testdb", charset="utf8")
# 使用cursor()方法获取操作游标 
cursor = db.cursor()

#start crawling product data from start to end of table product URL
start_number_one = 40559
while start_number_one < 45000:
    # SQL 查询语句
    sql_fetch_product_url_by_id = "SELECT product.product_URL FROM testdb.product where product.idproduct = %s"
    cursor.execute(sql_fetch_product_url_by_id, start_number_one)
    fetch_product_url_by_id_category_results = cursor.fetchone()
    product_url = fetch_product_url_by_id_category_results[0]
    #end of fetch product_url
    
    #start open and load a product URL
    #time_start = time.time()
    firefoxProfile = webdriver.FirefoxProfile()
    driver = webdriver.Firefox(firefox_profile=firefoxProfile)
    #driver = webdriver.PhantomJS('phantomjs')
    #handle_now = driver.current_window_handle
    #print('Time consuming 1:', time.time() - time_start)
    driver.get(product_url)
    #print('Time consuming 2:', time.time() - time_start)
    #driver.maximize_window()
    #print('Time consuming 3:', time.time() - time_start)
    #driver.switch_to_window(handle_now)
    #print('Time consuming 4:', time.time() - time_start)
    
    #等待图片显示
    #wait.until(lambda driver: driver.find_element_by_xpath('//div[@class="eg-step eg-step-1"]/a/div').is_displayed())
    #将窗口最大化 防止其他组件阻挡
    #if page not found, product url should be marked or deleted.
    '''#关闭跳出窗口
    try:
        click_the_window = driver.find_element_by_xpath('//div[@class="eg-step eg-step-1"]/a/div')
        driver.execute_script('$(arguments[0]).click()', click_the_window)
        #click_the_window.click()
    except NoSuchElementException as e:
        print('WARNING!! There is no clickable window 1')
    #another try to close the window
    try:
        click_the_window = driver.find_element_by_xpath('//div[@id="evergage-tooltip-ambiKWoo"]/a')
        driver.execute_script('$(arguments[0]).click()', click_the_window)
        #click_the_window.click()
    except NoSuchElementException as e:
        print('WARNING!! There is no clickable window 2')
        
    #尝试抓取product内容，存在已经撤销的链接，网站直接转到page not found页面
    #******************************************************'''
    try:
        crawlPageContent(driver)
    except NoSuchElementException as e:
        print('WARNING: PAGE NOT FOUND')
        sql_url_not_aviliable = """UPDATE testdb.product SET product_url_stat = %s WHERE idproduct = %s"""
        data = (0, start_number_one)
        cursor.execute(sql_url_not_aviliable, data)
        db.commit()#需要这一句才能保存到数据库中
        driver.quit()
    #End of crawling product content
    #************************************************************
    #关闭driver
    driver.quit()
    
    #迭代数字  start_number_one
    print(start_number_one)
    start_number_one = start_number_one + 1
    gc.collect()
db.close()