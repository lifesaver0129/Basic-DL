# -*- coding: utf-8 -*-
'''
Created on 2016年8月31日

@author: Administrator
'''
import pymysql, os
import shutil,os

def selectINFObyID(productID):
    output = ''
    #sqlstring = 'select idproduct, product_breadcrumbs, product_title, product_desc from origin_zalora.product where idproduct = %s'
    sqlstring = 'SELECT name FROM clean_data_zalora.category where code = (SELECT category FROM clean_data_zalora.product  where idproduct = %s)'
    cursor.execute(sqlstring, int(productID))
    fetch_result = cursor.fetchone()

    if fetch_result is not None:
        output = fetch_result[0]
    return output

def copyIMG(productID, category):
    
    sqlstring = 'SELECT product_sku FROM testdb.product where idproduct = %s'
    cursor.execute(sqlstring, int(productID))
    fetch_result = cursor.fetchone()
    IMG_path = ''
    if fetch_result is not None:
        IMG_path = fetch_result[0]
    
#     sourceIMGpath = '//158.132.122.218/pdata/' + IMG_path + '/' + '1.jpg' #ZALORA
    sourceIMGpath = '//158.132.122.218/pdata/ASOS/' + IMG_path.strip('asos') + '/' + '0.jpg'#H&M
    
    destinationFolder = 'C:/Users/Administrator/Desktop/ASOS_Recate_Women/'
    IMG_name = category + '_' + str(productID).zfill(6) + '.jpg'
    destinationFilePath = destinationFolder + IMG_name
    
    if not os.path.exists(destinationFolder):  ###判断文件是否存在，返回布尔值
        os.makedirs(destinationFolder)
    try:
        shutil.copyfile(sourceIMGpath, destinationFilePath)
        with open('C:/Users/Administrator/Desktop/output2.txt','a', encoding='utf8') as f:
            f.write(str(productID) + '\n')
    except:
        with open('C:/Users/Administrator/Desktop/output2.txt','a', encoding='utf8') as f:
            f.write(str(productID) + 'there is no such file:' + '\n')

db = pymysql.connect("localhost", "root", "123456", "testdb", charset="utf8")
cursor = db.cursor()

idandcategoryall = open("C:/Users/Administrator/Desktop/womenid.txt", encoding='utf8').readlines()

for eachrow in idandcategoryall:
    eachrow = eachrow.strip('\n')
    eachrowlist = eachrow.split('\t')
    eachid = int(eachrowlist[0])
    eachcategory = eachrowlist[1]
    if len(eachcategory) == 0:
        eachcategory = "NULL"
#     eachcategory = selectINFObyID(eachid)
    print(eachid)

    copyIMG(eachid, eachcategory)
    
db.close()
