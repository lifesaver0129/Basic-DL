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


def updateINFO(productID):
    sql_string = 'update `b2c-src`.product_maxmarch set productlist = %s where idproduct = %s'
    cursor.execute(sql_string, ('', productID))
    db.commit()

def selectByEmail(emailName):
    resultList = []
    sql_string = 'SELECT id_product, id_wishlist, wishlist_name FROM experiment.wishdetails where email = %s order by id_wishlist_product'
    cursor.execute(sql_string, emailName)

    fetch_result = cursor.fetchall()
    if fetch_result is not None:
        for ele in fetch_result:
            resultList.append(ele[0] + '\t' + ele[1]+ '\t' + ele[2])
    return resultList





def insertItem(contentList):
    # sql = 'INSERT INTO `b2c-src`.product_related (idproduct, productlist) VALUES (%s, %s)'
    sql = 'INSERT INTO experiment.wishdetails(id, id_customer, firstname, lastname, email, active, id_wishlist, \
    wishlist_name, counter, date_add, date_upd, id_wishlist_product, id_product, id_product_attribute, \
    quantity, priority) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
    data = (contentList[0], contentList[1], contentList[2], contentList[3], contentList[4], contentList[5] \
                , contentList[6], contentList[7], contentList[8], contentList[9], contentList[10], contentList[11] \
                , contentList[12], contentList[13], contentList[14], contentList[15])
    cursor.execute(sql, data)
    db.commit()


db = pymysql.connect(host="localhost",
                      user="root",
                      password="123456",
                      db="experiment",
                      charset="utf8")
cursor = db.cursor()



group1 = open("C:/Users/Administrator/Desktop/group1.txt", encoding='utf8').readlines()
group2 = open("C:/Users/Administrator/Desktop/group2.txt", encoding='utf8').readlines()
emaillist = open("C:/Users/Administrator/Desktop/email.txt", encoding='utf8').readlines()



idlist_group1 = []
namelist_group1 = []
codelist_group1 = []
for ele in group1:
    ele = ele.strip('\n')
    elelist = ele.split('\t')
    idlist_group1.append(elelist[0])
    namelist_group1.append(elelist[1])
    codelist_group1.append(elelist[2])


idlist_group2 = []
namelist_group2 = []
codelist_group2 = []
for ele in group2:
    ele = ele.strip('\n')
    elelist = ele.split('\t')
    idlist_group2.append(elelist[0])
    namelist_group2.append(elelist[1])
    codelist_group2.append(elelist[2])

# for ele in wishlist:
#     ele = ele.strip('\n')
#     elelist = ele.split('\t')
#     wishlist_type.append(elelist[0])
#     wishlist_id.append(elelist[1])


for eachemail in emaillist:
    eachemail = eachemail.strip('\n')
    eachperson_eachlist = selectByEmail(eachemail)

    for ele in eachperson_eachlist:
        type = ele.split('\t')[2]
        wishlistid = ele.split('\t')[1]

        ele = ele.split('\t')[0]

        groupname = ''
        if ele in idlist_group1:
            groupname = 'group1'
        if ele in idlist_group2:
            groupname = 'group2'

        with open('C:/Users/Administrator/Desktop/output.txt', 'a', encoding='utf8') as f:
            f.write(eachemail + '\t' + ele + '\t' + wishlistid + '\t' + type + '\t' + groupname + '\n')

db.close()
