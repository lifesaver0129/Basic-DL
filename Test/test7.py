#!/usr/bin/env python
# -*- coding: utf-8 -*-
import MyFunctions as MF
import pymysql
import re
import numpy as np

db = pymysql.connect("localhost", "root", "123456", charset="utf8")
cursor = db.cursor()
zalora = open("C:/Users/Administrator/Desktop/zalora.txt", encoding="utf8").readlines()


def find_info_by_ID(productID):
    outputlist = []

    sql_string = 'select product_title, product_brand, product_gender, product_price, product_desc, product_details from testdb.product where idproduct = %s'
    cursor.execute(sql_string, productID)
    fetch_result = cursor.fetchone()

    if fetch_result is not None:
        title = fetch_result[0].strip().lower()
        outputlist.append(title)#title

        brand = fetch_result[1].strip().lower()
        outputlist.append(brand)#brand

        outputlist.append(fetch_result[2])#gender

        price = re.findall(r'[\d,.]+', fetch_result[3])[0]
        outputlist.append(price.strip())#price



        descriptionList = MF.extract_nouns_from_string(fetch_result[4])#description
        description = MF.list_to_string(descriptionList).lower()
        outputlist.append(description)#description

        colour = ''
        if len(re.findall(r'Colour%[\w]+', fetch_result[5]))>0:
            colour = re.findall(r'Colour%[\w ]+', fetch_result[5])[0].replace('Colour%','')
        outputlist.append(colour.lower())  # description

    return outputlist

def insert_into_db(productInfoList):
    sql_string = 'INSERT INTO clean_data_zalora.product (idproduct, breadcrumbs, title, brand, gender, price, description, colour) \
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'
    data = (productID, bread, productInfoList[0], productInfoList[1], productInfoList[2], productInfoList[3], productInfoList[4], productInfoList[5])
    cursor.execute(sql_string, data)
    db.commit()#需要这一句才能保存到数据库中


def updateProductInfo(productID, infoList1, infoList2):
    print(productID)
    infoList = infoList1.replace(',', '')
    deslist = re.findall(r'[a-z]{3,}\b|[\u4e00-\u9fa5]+', infoList2)
    descritpion = MF.list_to_string(deslist)

    sql_string = 'UPDATE clean_data_zalora.product SET price = %s, description = %s WHERE idproduct = %s'
    data = (infoList, descritpion, productID)
    cursor.execute(sql_string, data)
    db.commit()#需要这一句才能保存到数据库中




for each_line in zalora:
    each_line = each_line.strip('\n')
    each_lineList = each_line.split('\t')

    productID = each_lineList[0].strip()
    price = each_lineList[1].strip()
    desc = each_lineList[2].strip()
    #
    # productInfoList = find_info_by_ID(productID)
    # print(productID)
    #
    #
    # insert_into_db(productInfoList)
    updateProductInfo(productID, price, desc)
db.close()