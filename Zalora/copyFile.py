'''
Created on 2017年1月3日

@author: Administrator
'''

import shutil,os

import pymysql

db = pymysql.connect("localhost","root","123456","testdb", charset="utf8")
#     db = pymysql.connect("158.132.123.119","root","tozmartdev2016","b2c-zw", 13306, charset="utf8")
    # 使用cursor()方法获取操作游标 
cursor = db.cursor()
    
zaloraProducts = open("C:/Users/Administrator/Desktop/zalora_id.txt").readlines()


for productID in zaloraProducts:
    productID = productID.strip('\n')
    print(productID)
    sqlString = 'select product_img_number, product_img_path from test.product where idproduct = %s'
    cursor.execute(sqlString, productID)
    fetch_result = cursor.fetchall()
    img_num = 0
    img_path = ''
    img_new_name = ''
    img_new_path = 'F:/Zalora For YH/'
    if not os.path.exists(img_new_path):  ###判断文件是否存在，返回布尔值
        os.makedirs(img_new_path)
        
    if fetch_result is not None:
        for ele_fetch_result in fetch_result:
            img_num = int(ele_fetch_result[0])
            img_path = ele_fetch_result[1]
            
    if img_num > 0:
        for inumber in range(img_num):

            img_path_old = 'F:/' + img_path + '/' + str(inumber + 1) + '.jpg'
            img_new_name = str(productID) + '_' + str(inumber + 1) + '.jpg'
            if not os.path.exists(img_new_path + str(inumber + 1) + '/'):  ###判断文件是否存在，返回布尔值
                os.makedirs(img_new_path + str(inumber + 1) + '/')
            shutil.copyfile(img_path_old, img_new_path + str(inumber + 1) + '/' + img_new_name)

db.close()
    
    
