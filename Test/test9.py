#!/usr/bin/env python
# -*- coding: utf-8 -*-

import MyFunctions as MF
import pymysql


def delproduct(productID):
    sql_string = 'delete from `b2c-src`.product where idproduct = %s'
    cursor.execute(sql_string, productID)
    db.commit()

def updateINFO(productID, newbread):
    sql_string = 'update `b2c-src`.product set product_breadcrumbs = %s where idproduct = %s'
#    sql_string = 'update `b2c-src`.product_related set productlist = %s where idproduct = %s'
    cursor.execute(sql_string, (newbread, productID))
    db.commit()

def selectINFO(productID):
    output = ''
    sql_string = 'select product_img_path from testdb.product where idproduct = %s'
    cursor2.execute(sql_string, productID)
    fetch_result = cursor2.fetchone()
    if fetch_result is not None:
        output = fetch_result[0]
    return output

def insertItem(productID, content):
    # sql = 'INSERT INTO `b2c-src`.product_related (idproduct, productlist) VALUES (%s, %s)'
    sql = 'INSERT INTO `b2c-src`.product_maxmarch (idproduct, productlist) VALUES (%s, %s)'

    cursor.execute(sql, (productID, content))
    db.commit()


db = pymysql.connect("158.132.122.212", "root", "tozmartdev2016", "b2c-src", 13306, charset="utf8")
cursor = db.cursor()

db2 = pymysql.connect(host="localhost",
                      user="root",
                      password="123456",
                      db="origin_zalora",
                      charset="utf8")
cursor2 = db2.cursor()



products = open("C:/Users/Administrator/Desktop/idcategory.txt", encoding='utf8').readlines()

for ele in products:
    ele = ele.strip('\n')
    elelist = ele.split('\t')
    id = elelist[0]
    cate = elelist[1]
    feature = elelist[2]

    print(id)

    path = selectINFO(id)
    print(path)
    with open('C:/Users/Administrator/Desktop/ForYH.txt', 'a', encoding='utf8') as f:
        f.write(str(id) + '\t' + str(path) + '\t' + str(cate) + '\t' + str(feature) + '\n')

db.close()
db2.close()