import pymysql, nltk
import re, random
import numpy as np

db = pymysql.connect("localhost", "root", "123456", "clean_data_zalora", charset="utf8")
cursor = db.cursor()

zalora = open("C:/Users/Administrator/Desktop/id.txt", encoding="utf8").readlines()

for ele in zalora:
    ele = ele.strip('\n')
    print(ele)

    sql1 = 'update product set category = %s where idproduct = %s'

    cursor.execute(sql1, ('T304', int(ele)))
    db.commit()  # 需要这一句才能保存到数据库中

db.close()
