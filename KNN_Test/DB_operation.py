# -*- coding: utf-8 -*-
import pymysql
import numpy as np


def write_db_info(sql_string, datalist):
    cursor.execute(sql_string, datalist)
    db.commit()#需要这一句才能保存到数据库中


if __name__ == '__main__':
    db = pymysql.connect("localhost","root","123456","testdb", charset="utf8")
    cursor = db.cursor()
    attributes = open("C:/Users/Administrator/Desktop/attributes.txt").readlines()
    
    for each_att in attributes:
        each_att = each_att.strip('\n')
        each_attList = each_att.split('\t')
        pid = each_attList[0]
        pcate = each_attList[1]
        pattribute = each_attList[2]
        p_hash = each_attList[3]
        print(pid)
        
        datalist = (pid, pcate, pattribute, p_hash)
        sql_string = 'INSERT INTO hashing_test.product_attributes (idproduct, category, attribute_1, attribute_1_hashing) VALUES (%s,%s,%s,%s)'
        write_db_info(sql_string, datalist)
        
