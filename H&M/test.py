'''
Created on 2016年11月9日

@author: Administrator
'''


import pymysql

filep = open('C:/Users/Administrator/Desktop/hm.txt')
file = filep.readlines()
db = pymysql.connect("localhost","root","123456","testdb", charset="utf8")
# 使用cursor()方法获取操作游标 
cursor = db.cursor()


for e in file:
    e = e.strip()
    product_list = []
    sql = 'select idproduct from testdb.product where product_breadcrumbs = %s'
    
    cursor.execute(sql, e)
    fetch_productList_by_id_results = cursor.fetchall()
    
    if fetch_productList_by_id_results[0] is not None:
        for ele in fetch_productList_by_id_results:
            product_list.append(ele[0])
            
    with open('C:/Users/Administrator/Desktop/resulthm.txt','a') as f: 
        f.write(e + '\t' + str(product_list) + '\n')
    
    
filep.close()
db.close()