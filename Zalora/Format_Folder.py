'''
Created on 2016年8月15日

@author: Administrator
'''


import os,pymysql
import shutil


db = pymysql.connect("localhost","root","123456","testdb", charset="utf8")
# 使用cursor()方法获取操作游标 
cursor = db.cursor()

product_id_number = 10000
folder_number_start = 45635
while product_id_number < 76543:
    # SQL 查询语句
    root_path = 'C:/Users/Administrator/Desktop/'
    img_path = 'C:/Users/Administrator/Desktop/p/'
    sql_fetch_product_url_by_id = "SELECT product_img_path, product_img_number FROM product where idproduct = %s"
    cursor.execute(sql_fetch_product_url_by_id, product_id_number)
    fetch_product_url_by_id_category_results = cursor.fetchone()
    if fetch_product_url_by_id_category_results[0] is not None:
        product_img_path = str(fetch_product_url_by_id_category_results[0])
        product_img_number = int(fetch_product_url_by_id_category_results[1])
        if len(product_img_path) != 0:
            num_zero = 1
            product_image = ''
            while num_zero < product_img_number + 1:
                product_image = product_image + str(folder_number_start) + ';'
                img_path_new = img_path + str(folder_number_start)
                if not os.path.exists(img_path_new):  ###判断文件是否存在，返回布尔值
                    os.makedirs(img_path_new)
                img_path_old = root_path + product_img_path + '/' + str(num_zero) + '.jpg'
                print(img_path_old)
                img_path_new = img_path_new + '/' + str(folder_number_start) + '.jpg'
                print(img_path_new)
                shutil.copyfile(img_path_old, img_path_new)
                folder_number_start = folder_number_start + 1
                num_zero = num_zero + 1
            #update product_img_fids here
            sql_update_fids = """UPDATE testdb.product SET product_img_fids = %s WHERE idproduct = %s"""
            data = (product_image, product_id_number)
            cursor.execute(sql_update_fids, data)
            db.commit()#需要这一句才能保存到数据库中
            print(product_image)
    product_id_number = product_id_number + 1
    
db.close()
