#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2017年1月12日

@author: Administrator
'''

import MyFunctions as MF
import pymysql


def findidlist(category):
    outputlist = []
    sqlstring = 'SELECT idproduct FROM testdb.product where product_breadcrumbs = %s'
    cursor.execute(sqlstring, category)
    fetch_result = cursor.fetchall()

    if fetch_result is not None:
        for ele_fetch_result in fetch_result:
            outputlist.append(ele_fetch_result[0])
    return outputlist

def findidlist2(category):
    outputlist = []
    sqlstring = 'SELECT idproduct FROM `1`.product where category = %s'
    cursor.execute(sqlstring, category)
    fetch_result = cursor.fetchall()

    if fetch_result is not None:
        for ele_fetch_result in fetch_result:
            outputlist.append(ele_fetch_result[0])
    return outputlist


db = pymysql.connect(host="localhost",
                         user="root",
                         password="123456",
                         db="clean_data_zalora",
                         charset="utf8")
cursor = db.cursor()


oldCategoryList = open("C:/Users/Administrator/Desktop/oldcate.txt", encoding='utf8').readlines()
newCategoryList = open("C:/Users/Administrator/Desktop/newcate.txt", encoding='utf8').readlines()
idandcate = open("C:/Users/Administrator/Desktop/info.txt", encoding='utf8').readlines()

oldlist = []
for ele in oldCategoryList:
    ele = ele.strip('\n')
    oldlist.append(ele)

newlist = []
for ele in newCategoryList:
    ele = ele.strip('\n')
    newlist.append(ele)


for ele in newlist:
    print(ele)
    oldcategoryList = []
    newcategoryList = []
    oldcategoryList = findidlist(ele)
    newcategoryList = findidlist2(ele)
    chaji = list(set(oldcategoryList).difference(set(newcategoryList)))
    chaji2 = list(set(newcategoryList).difference(set(oldcategoryList)))

    with open('C:/Users/Administrator/Desktop/output3.txt', 'a', encoding='utf8') as f:
        f.write(ele + '\t' + str(chaji) + '\t' + str(chaji2) + '\n')
