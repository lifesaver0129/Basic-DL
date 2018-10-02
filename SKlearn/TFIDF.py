# -*- coding: utf-8 -*-

import pymysql, os
import shutil,os

db = pymysql.connect("localhost", "root", "123456", "testdb", charset="utf8")
cursor = db.cursor()

idalls = open("C:/Users/Administrator/Desktop/ids.txt", encoding='utf8').readlines()

def selectINFObyID(productID):
    path = ''
    number = 0
    
    #sqlstring = 'select idproduct, product_breadcrumbs, product_title, product_desc from origin_zalora.product where idproduct = %s'
    sqlstring = 'SELECT product_sku, product_img_number FROM testdb.product where idproduct= %s'
    cursor.execute(sqlstring, int(productID))
    fetch_result = cursor.fetchone()

    if fetch_result is not None:
        path = fetch_result[0]
        number = fetch_result[1]
    return path, number

for eachrow in idalls:
    eachrow = eachrow.strip('\n')
    print(eachrow)
    product_path, product_number = selectINFObyID(eachrow)
    with open('C:/Users/Administrator/Desktop/pathandnumber.txt','a', encoding='utf8') as f:
        f.write(str(eachrow) + '\t' + product_path + '\t'  + str(product_number) + '\t' + '\n')
    
db.close()
