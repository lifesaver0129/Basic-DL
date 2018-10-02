'''
Created on 2016年12月20日

@author: Administrator
'''
import pymysql


db = pymysql.connect("158.132.123.119","root","tozmartdev2016","b2c-src", 13306, charset="utf8")
cursor = db.cursor()

recommendation = open("C:/Users/Administrator/Desktop/recommendation_list.txt", encoding='utf8').readlines()

for ele_recommendation in recommendation:
    ele_recommendation = ele_recommendation.strip('\n')
    eleList = ele_recommendation.split('\t')
    productID = eleList[0]
    print(productID)
    recString = eleList[1]
    if len(recString) > 0:
        sqlString = 'UPDATE product_related  SET productlist = %s WHERE idproduct = %s'
        data = (recString, productID)
        cursor.execute(sqlString, data)
        db.commit()#需要这一句才能保存到数据库中
    

    
