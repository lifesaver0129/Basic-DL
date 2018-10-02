#!/usr/bin/env python2
#-*-encoding:utf-8-*-
'''
Created on 2016年8月3日
@author: Administrator
'''
import csv, os
import pymysql

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
#incease_num = 1

# 打开数据库连接
db = pymysql.connect("localhost","root","123456","testdb" )
# 使用cursor()方法获取操作游标 
cursor = db.cursor()

#注入URL进入数据库
for file_elment in category_list:
    # SQL 查询语句
    category_name = str(file_elment)
    category_name = category_name.replace("%", "/");
    #获取category id
    sql_fetch_category_id_by_name = "SELECT category.category_code FROM testdb.category where category_name = %s"
    # 执行SQL语句 注意sql变量的表示方法
    cursor.execute(sql_fetch_category_id_by_name,category_name)
    # 获取所有记录列表
    results = cursor.fetchone()
    #得到url所属于的category
    url_filename_category = str(results[0])
    #print(url_filename_category)

    file_name = str(file_elment) + '.csv'
    each_file_url_list = readURL(dir_path + 'urls/', file_name)
    print("The file name is:" + file_name)
    #存入URL到数据库中
    try:
        for each_url in each_file_url_list:
            #判断URL是否已经存在于数据库中
            sql_existing_url = """SELECT product.product_category FROM testdb.product where product_URL = %s"""
            # 执行SQL语句 注意sql变量的表示方法
            cursor.execute(sql_existing_url,each_url)
            # 获取所有记录列表
            url_category_results = cursor.fetchone()
            
            #判断URL是否存在，results是否为None
            if url_category_results is None:#if the query result is None: INSERT
                insert_data = (each_url,url_filename_category)
                sql_insertinto_url = """INSERT INTO testdb.product(product_URL,product_category) VALUES(%s,%s)"""
                cursor.execute(sql_insertinto_url,insert_data)
                db.commit()#需要这一句才能保存到数据库中
                #emp_no = cursor.lastrowid
                #print(emp_no)
            if url_category_results is not None:#if the query result is None: UPDATE
                category_string = str(url_category_results[0])
                print(category_string)
                if url_filename_category not in category_string:
                    new_category_string = url_filename_category + ';' + category_string
                    #print(url_filename_category)
                    #print(category_code ,inerting_url)
                    sql_update_url = """UPDATE testdb.product SET product_category = %s WHERE product_URL = %s"""
                    update_data = (new_category_string, each_url)
                    cursor.execute(sql_update_url,update_data)
                    db.commit()#需要这一句才能保存到数据库中
        #删除该文件
        os.remove(dir_path + 'urls/' + file_name)
    except:
        print('NoneType line contains NULL byte: object is not iterable')
        #得到url所属于的category
