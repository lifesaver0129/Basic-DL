
import pymysql
import re

def set_price_level(listOfProductPrice):
    level_low = 0
    level_high = 0
    lenthOfList = len(listOfProductPrice)

    listOfProductPrice = sorted(listOfProductPrice)
    if lenthOfList > 3:
        level_low = listOfProductPrice[round(0.3*lenthOfList)]
        level_high = listOfProductPrice[round(0.7*lenthOfList)]

    if lenthOfList == 3:
        level_low = listOfProductPrice[1]
        level_high = listOfProductPrice[1]

    if lenthOfList == 2:
        level_low = listOfProductPrice[0]
        level_high = listOfProductPrice[1]

    if lenthOfList == 1:
        level_low = listOfProductPrice[0]
        level_high = listOfProductPrice[0]

    return level_low, level_high


zalora = open("C:/Users/Administrator/Desktop/product_category_zalora.txt", encoding='utf8').readlines()

db = pymysql.connect("localhost","root","123456","test", charset="utf8")
cursor = db.cursor()

for ele in zalora:
    ele = ele.strip('\n')
    stringsql = 'select product_price from testdb.product where product_breadcrumbs = %s'
    cursor.execute(stringsql, ele)
    fetch_result = cursor.fetchall()
    pricelist = []

    for ele_fetch_result in fetch_result:
        pricelst = re.findall(r'[0-9]+[.]*[0-9]*', ele_fetch_result[0])[0]
        pricelist.append(pricelst)
    level_low, level_high = set_price_level(pricelist)
    print(level_low, level_high)

