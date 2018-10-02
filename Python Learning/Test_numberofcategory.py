# -*- coding: utf-8 -*-
import pymysql

def selectINFObyID(productID):
    output = ''
    sqlstring = 'SELECT product_desc FROM testdb.product where idproduct = %s'
    cursor.execute(sqlstring, int(productID))
    fetch_result = cursor.fetchone()

    if fetch_result is not None:
        output = fetch_result[0]
    return output

idproducts = open("C:/Users/Administrator/Desktop/idproducts.txt", encoding='utf8').readlines()
db = pymysql.connect("localhost", "root", "123456", "testdb", charset="utf8")
cursor = db.cursor()

for ele in idproducts:
    ele = ele.strip('\n')
    details = selectINFObyID(ele)
    
    if details is not None and len(details) > 10:
        details = details.replace('\n', ' ').replace('\r', ' ')
        with open('C:/Users/Administrator/Desktop/final.txt','a', encoding='utf8') as f:
            f.write(details + '\n')


