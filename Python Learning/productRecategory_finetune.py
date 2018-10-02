# -*- coding: utf-8 -*-
'''
Created on 2016年8月31日

@author: Administrator
'''
import MyFunctions as MF
import pymysql


def selectINFObyID(productID):
    output = ''
    #sqlstring = 'select idproduct, product_breadcrumbs, product_title, product_desc from origin_zalora.product where idproduct = %s'
    sqlstring = 'SELECT name FROM clean_data_zalora.category where code = (SELECT category FROM clean_data_zalora.product  where idproduct = %s)'
    cursor.execute(sqlstring, int(productID))
    fetch_result = cursor.fetchone()

    if fetch_result is not None:
        output = fetch_result[0]
    return output


db = pymysql.connect("localhost", "root", "123456", "clean_data_zalora", charset="utf8")
cursor = db.cursor()

cleanids = open("C:/Users/Administrator/Desktop/votewomen.txt", encoding='utf8').readlines()
priorules = open("C:/Users/Administrator/Desktop/womenprio.txt", encoding='utf8').readlines()

bigcateList = []
smallcateList = []

for ele in priorules:
    elelist = ele.strip('\n').lower().split(';')
    bigcateList.append(elelist[0])
    smallcateList.append(elelist[1:])

for eachrow in cleanids:
    newcategory = ''
    eachrow = eachrow.strip('\n')
    eachrowlist = eachrow.split('\t')
    eachid = int(eachrowlist[0])
    breadlist = eachrowlist[1].split(';')
    titlelist = eachrowlist[2].split(';')
    desclist = eachrowlist[3].split(';')
    listtall = breadlist + titlelist + desclist
    listsingle = []
    for ele in listtall:
        if ele not in listsingle and len(ele)>0:
            listsingle.append(ele)
    listnumber = []
    
    for ele in listsingle:#计算每个的数量
        elecount = 0
        elecount = 4*breadlist.count(ele) + 2*titlelist.count(ele) + 0.5*desclist.count(ele)
        listnumber.append(elecount)
    
    print(eachid)
    
    if len(listnumber) > 0:
        newcategory = listsingle[listnumber.index(max(listnumber))]
        if newcategory in bigcateList:
            for ele in smallcateList[bigcateList.index(newcategory)]:
                if len(ele) > 0 and ele in listtall:
                    newcategory = ele
        
        with open('C:/Users/Administrator/Desktop/output.txt','a', encoding='utf8') as f:
            f.write(str(eachid) + '\t' + newcategory + '\n')
    else:
        with open('C:/Users/Administrator/Desktop/output.txt','a', encoding='utf8') as f:
            f.write(str(eachid) + '\t' + newcategory + '\n')
