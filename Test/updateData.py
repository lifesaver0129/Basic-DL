#!/usr/bin/env python
# -*- coding: utf-8 -*-

import MyFunctions as MF
import pymysql
import re, random
import numpy as np

def selectINFO(productID):
    output = ''
    sql_string = 'select productlist from `b2c-src`.product_maxmarch where idproduct = %s'
    cursor.execute(sql_string, productID)
    fetch_result = cursor.fetchone()
    if fetch_result is not None:
        output = fetch_result[0]
    return output


def updateINFO(productID):
    sql_string = 'update `b2c-src`.product_maxmarch set productlist = %s where idproduct = %s'
#    sql_string = 'update `b2c-src`.product_related set productlist = %s where idproduct = %s'
    cursor.execute(sql_string, ('', productID))
    db.commit()

db = pymysql.connect("158.132.122.212", "root", "tozmartdev2016", "b2c-src", 13306, charset="utf8")
cursor = db.cursor()

def insertItem(id, content):
    sql = 'INSERT INTO `b2c-src`.product_maxmarch (idproduct,productlist) VALUES (%s, %s)'
    cursor.execute(sql, (id, content))
    db.commit()

def delproduct(productID):
    sql = 'delete from `b2c-src`.product_maxmarch where idproduct = %s'
    cursor.execute(sql, (id, productID))
    db.commit()



group1products = open("C:/Users/Administrator/Desktop/group1.txt", encoding='utf8').readlines()

# mixmatchs = open("C:/Users/Administrator/Desktop/maxmatch.txt", encoding='utf8').readlines()

group1_list = []
for ele in group1products:
    ele = ele.strip('\n')
    group1_list.append(ele)

for product in group1_list:
    print(product)
    updateINFO(product)

db.close()
