#!/usr/bin/env python
# -*- coding: utf-8 -*-

import MyFunctions as MF
import pymysql
import re, random
import numpy as np

def selectINFO(productID):
    output = ''
    sql_string = 'select productlist from `b2c-src`.product_related where idproduct = %s'
    cursor.execute(sql_string, productID)
    fetch_result = cursor.fetchone()
    if fetch_result is not None:
        output = fetch_result[0]
    return output


def updateINFO(productID):
    sql_string = 'update `b2c-src`.product_maxmarch set productlist = %s where idproduct = %s'
    cursor.execute(sql_string, ('', productID))
    db.commit()

db = pymysql.connect("158.132.122.211", "root", "tozmartdev2016", "b2c-zw", 13306, charset="utf8")
cursor = db.cursor()



products = open("C:/Users/Administrator/Desktop/product.txt", encoding='utf8').readlines()
for product in products:
    product = product.strip('\n')
    print(product)
    relatedproducts = updateINFO(product)

db.close()
