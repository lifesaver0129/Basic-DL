# -*- coding: utf-8 -*-

from scipy import spatial
import pymysql


def load_info_by_id(product_id):
    outputList = []
    sql_string = 'select attribute_1 from hashing_test.product_attributes where idproduct = %s'
    
    cursor.execute(sql_string, product_id)
    fetch_result = cursor.fetchone()
    
    if fetch_result is not None:
        outputList = fetch_result[0].split(';')
    outputList = [float(i) for i in outputList]
    return outputList

    

if __name__ == '__main__':
    db = pymysql.connect("localhost","root","123456","testdb", charset="utf8")
    cursor = db.cursor()
    p_ids = open("C:/Users/Administrator/Desktop/ids.txt").readlines()
    
    target_id = 298
    anslist = []
    for ele in p_ids:
        ele = ele.strip('\n')
        result = 1 - spatial.distance.cosine(load_info_by_id(target_id), load_info_by_id(int(ele)))
        anslist.append(result)
    print(sorted(anslist))
