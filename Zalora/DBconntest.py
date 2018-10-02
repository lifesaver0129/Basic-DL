#!/usr/bin/python3
# -*- coding: UTF-8 -*-


import pymysql
import csv, os
from _overlapped import NULL



def readURL(dir_path, file_name):
    #写入csv文件 文件名
    LIST = []
    f = open(dir_path + file_name)
    reader = csv.reader(f)
    try:
        for line in reader:
            LIST.append(line[0])
        return LIST
        f.close()
    except:
        print('line contains NULL byte')
        f.close()

def GetFileNameAndExt(filename):
    shot_name, ext_name = filename.split('.')
    return shot_name


def walk_dir(dir_path,fileinfo,topdown=True):
    for root, dirs, files in os.walk(dir_path, topdown):
        for name in files:
            category_name = GetFileNameAndExt(os.path.join(name))
            print(category_name)


dir_path = 'C:/Users/Administrator/Desktop/'

#category name of all categories.读取这个目录下的所有文件名
category_list = readURL(dir_path,"1.csv")


# 打开数据库连接
db = pymysql.connect("localhost","root","123456","testdb" )

# 使用cursor()方法获取操作游标 
cursor = db.cursor()
# SQL 查询语句
category_name = 'Men'
sql_fetch_category_id_by_name = "SELECT category.category_code FROM testdb.category where category_name = %s"

cursor.execute(sql_fetch_category_id_by_name,category_name)
category_results = cursor.fetchone()
    # 获取 category_code 管用
category_code = str(category_results[0])

inerting_url = 'https://www.zalora.com.hk/dandelion-pu-star-denim-snapback-%E8%97%8D%E8%89%B2-4607360.html'
sql_exist_url = "SELECT product.product_category FROM testdb.product where product_URL = %s"
#获取已经存在的url管用
cursor.execute(sql_exist_url,inerting_url)
url_category_results = cursor.fetchone()
print(url_category_results)

if url_category_results is None:#if the query result is None:
    sql_insertinto_url = "INSERT INTO testdb.product(product_URL,product_category) VALUES('fuck you','fuck')"
    cursor.execute(sql_insertinto_url)
    db.commit()#需要这一句才能保存到数据库中
if url_category_results is not None:#if the query result is None:
    for result in url_category_results:
        print(result)
        print(category_code)
        if category_code not in result:
            print('fuck')
            category_code = category_code + ';' + result
            print(category_code)
            #print(category_code ,inerting_url)
            sql_update_url = """UPDATE testdb.product SET product_category = %s WHERE product_URL = %s"""
            data = (category_code, inerting_url)
            cursor.execute(sql_update_url,data)
            db.commit()#需要这一句才能保存到数据库中
# 关闭数据库连接
cursor.close()
db.close()
