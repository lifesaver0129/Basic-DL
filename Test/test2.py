
import numpy as np
import pymysql,re


def updatebyid(ele_productID, bread, gender, cate, feature):
    sql = 'UPDATE clean_data_zalora.product SET breadcrumbs = %s, gender = %s, category = %s, feature = %s WHERE idproduct = %s'
    data = (bread, gender, cate, feature, ele_productID)
    cursor.execute(sql, data)
    db.commit()


def selectbyid(productID):
    outputList = ''
    sqlString = "select breadcrumbs from clean_data_zalora.product where idproduct = %s"

    cursor.execute(sqlString, productID)
    fetch_result = cursor.fetchone()

    if fetch_result is not None:
        for ele in fetch_result:
            outputList = ele
    return outputList

def delitem(id):
    sql = "DELETE FROM clean_data_zalora.product WHERE idproduct = %s"
    cursor.execute(sql, id)
    db.commit()


db = pymysql.connect("localhost", "root", "123456", "clean_data_zalora", charset="utf8")
cursor = db.cursor()

zalora = open("C:/Users/Administrator/Desktop/test.txt", encoding='utf8').readlines()

for eachrow in zalora:
    eachrow = eachrow.strip('\n')
    print(eachrow)
    delitem(eachrow)






#     eachrow = eachrow.strip('\n').strip(';')
#     eachrowlist = eachrow.split('\t')
#
#     productList = eachrowlist[0].split(';')
#     bread = eachrowlist[1]
#     gender = eachrowlist[2]
#     cate = eachrowlist[3]
#
#     feature = eachrowlist[4]
#
#     for ele_productID in productList:
#         ele_productID = ele_productID.strip()
#         if len(ele_productID) > 0:
#             breadpath = selectbyid(ele_productID)
#             # ele_productID = 660
#             # if breadpath != bread:
#             if breadpath != '' and breadpath != bread:
#                 print(ele_productID)
#                 updatebyid(ele_productID, bread, gender, cate, feature)
#         # if bread != breadpath:
#         #     print(bread, breadpath)
# # updatebyid(ele_productID, bread, gender, cate, feature)


db.close()