'''
Created on 2017年1月6日

@author: Administrator
'''
import MyFunctions as MF
import pymysql, nltk
import re, random
import numpy as np

def find_productID(category,categorycode,matchcategory,matchcategorycode,score,gender):
    output = 0
    stringsql = 'select idmatch from clean_data_zalora.mix_match_pairs where category = %s and categorycode = %s and matchcategory = %s and matchcategorycode = %s and score = %s and gender = %s'
    cursor.execute(stringsql, (category,categorycode,matchcategory,matchcategorycode,score,gender))
    fetch_result = cursor.fetchone()
    output = fetch_result[0]
    return output
    

db = pymysql.connect(host="localhost",
                     user="root",
                     password="123456",
                     db="clean_data_zalora",
                     charset="utf8")
cursor = db.cursor()
zaloraProducts = open("C:/Users/Administrator/Desktop/test.txt", encoding='utf8').readlines()

for ele in zaloraProducts:
    ele = ele.strip('\n')
    stringsql = 'SELECT parent_code FROM clean_data_zalora.category where code = %s'
    cursor.execute(stringsql, ele)
    fetch_result = cursor.fetchone()
    output = fetch_result[0]
    print(ele + '\t' + output)
#     elelist = ele.split('\t')
#     
#     category = elelist[0]
#     categorycode = elelist[1]
#     
#     matchcategory = elelist[2]
#     matchcategorycode = elelist[3]
#     
#     score = elelist[4]
#     gender = elelist[5]
#     tag = elelist[6]
#     
#     productID = find_productID(category,categorycode,matchcategory,matchcategorycode,score,gender)
#     
#     sqlstring = 'update clean_data_zalora.mix_match_pairs set category = %s, categorycode = %s, matchcategory = %s, matchcategorycode = %s, score = %s, gender = %s, level = %s where idmatch = %s'
#     
#     cursor.execute(sqlstring, (category,categorycode,matchcategory,matchcategorycode,score,gender,tag,productID))
#     db.commit()#需要这一句才能保存到数据库中

db.close()
