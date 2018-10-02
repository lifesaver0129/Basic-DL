'''
Created on 2016年9月28日

@author: Administrator
'''
import os, time, urllib, pymysql
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException    
import shutil
ISOTIMEFORMAT='%Y-%m-%d %X'    #Time setup

def get_folder_path_by_IMG_id(imgid):
    imgid = str(imgid)
    string_path = ''
    for ele in imgid:
        string_path = string_path + ele + '/'
    return string_path

def get_product_img_fids(product_img_number, img_id_start):
    string_fids = ''
    img_id_end = img_id_start + int(product_img_number)
    while img_id_start < img_id_end:
        string_fids = string_fids + str(img_id_start) + ";"
        img_id_start = img_id_start + 1
    return string_fids.rstrip(";")

#begin the main function
#connect the database.
db = pymysql.connect("localhost","root","123456","testdb", charset="utf8")
# 使用cursor()方法获取操作游标 
cursor = db.cursor()

product_id_start = 76553
img_id_start = 324171


sql_query_select = """SELECT product.product_img_fids, product.product_sku from product where idproduct = %s"""
sql_query_update = """UPDATE testdb.product SET product_img_fids = %s WHERE idproduct = %s"""
home_folder = "C:/Users/Administrator/Desktop/H&M/"
new_home_folder = "C:/Users/Administrator/Desktop/new_H&M/"

while product_id_start < 78891:
    # 执行SQL语句 注意sql变量的表示方法
    cursor.execute(sql_query_select, product_id_start)
    # 获取所有记录列表
    results = cursor.fetchone()
    #得到url所属于的category
    product_img_string = results[0]
    product_sku = results[1]
     
    img_list = product_img_string.split(';')
    
    img_nmber = 0
    for ele in img_list:
        new_path_ = ''
        new_path_ = new_home_folder + get_folder_path_by_IMG_id(ele)
        if not os.path.exists(new_path_):  ###判断文件是否存在，返回布尔值
            os.makedirs(new_path_)
        shutil.copy(home_folder + product_sku + "/" + str(img_nmber) + ".jpg", new_path_ + str(ele) + ".jpg")
        img_nmber = img_nmber + 1
#     product_img_fids = get_product_img_fids(product_img_number, img_id_start)
#     print(product_img_fids)
#     
#     img_id_start = img_id_start + product_img_number
#     
#     update_data = (product_img_fids, product_id_start)
#     cursor.execute(sql_query_update, update_data)
#     db.commit()#需要这一句才能保存到数据库中
    
    product_id_start = product_id_start + 1
#     
db.close()