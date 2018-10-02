
import re, pymysql
import numpy as np

db = pymysql.connect("localhost", "root", "123456", "test", charset="utf8")
cursor = db.cursor()
zalora = open("C:/Users/Administrator/Desktop/zalora_id.txt", encoding='utf8').readlines()
for productID in zalora:
    productID = productID.strip('\n')
    gender = 0
    productName = ''
    productCode = ''
    sqlstring = 'select product_gender, category_1_lvl from test.product where idproduct = %s'
    cursor.execute(sqlstring, productID)
    fetch_result = cursor.fetchone()

    if fetch_result is not None:
        gender = fetch_result[0]
        productName = fetch_result[1]

    sqlstring2 = 'select code from test.category where gender = %s and name = %s'
    cursor.execute(sqlstring2, (gender, productName))
    fetch_result = cursor.fetchone()
    if fetch_result is not None:
        productCode = fetch_result[0]


    sqlstring3 = 'update test.product set category_1_lvl = %s where idproduct = %s'
    cursor.execute(sqlstring3, (productCode, productID))
    db.commit()  # 需要这一句才能保存到数据库中

db.close()
