'''
Created on 2016年12月22日

@author: Administrator
'''
import re, pymysql
import MyFunctions as MF
zalora = open("C:/Users/Administrator/Desktop/input.txt", encoding='utf8').readlines()

db = pymysql.connect("localhost","root","123456","test", charset="utf8")
cursor = db.cursor()

sqlstring = 'select code from test.category where name = %s and gender = %s'

for ele in zalora:
    ele = ele.strip('\n')
    elelst = ele.split('\t')
    gender = elelst[0]
    category_name = elelst[1]
    
    cursor.execute(sqlstring, (category_name, gender))
    fetch_result = cursor.fetchone()
    if fetch_result is not None:
        code = fetch_result[0]
        print(code)
    else:                    
        print(gender + '\t' + category_name + '\n')
