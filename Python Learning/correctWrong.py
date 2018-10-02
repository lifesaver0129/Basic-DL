# -*- coding: utf-8 -*-

import pymysql
import re

ids = open("C:/Users/Administrator/Desktop/ids.txt").readlines()

def selectINFObyID(productID):
    output = ''
    #sqlstring = 'select idproduct, product_breadcrumbs, product_title, product_desc from origin_zalora.product where idproduct = %s'
    sqlstring = 'SELECT product_desc FROM testdb.product where idproduct = %s'
    cursor.execute(sqlstring, int(productID))
    fetch_result = cursor.fetchone()

    if fetch_result is not None:
        output = fetch_result[0].strip('\n').strip('\r')
    return output



def selectINFObyID2(productID):
    output = ''
    #sqlstring = 'select idproduct, product_breadcrumbs, product_title, product_desc from origin_zalora.product where idproduct = %s'
    sqlstring = 'SELECT product_details FROM testdb.product where idproduct = %s'
    cursor.execute(sqlstring, int(productID))
    fetch_result = cursor.fetchone()

    if fetch_result is not None:
        try:
            output = fetch_result[0].strip('\n').strip('\r')
        except:
            output = ''
    return output


db = pymysql.connect("localhost", "root", "123456", "testdb", charset="utf8")
cursor = db.cursor()

allproductsList = []
    
allList = []
singlelist = []
for each_id in ids:
    each_id = each_id.strip('\n')
    material = ''
     
    material = selectINFObyID(each_id).lower()
#     material_list = re.findall(r'%[ ]*[a-z]+[ ]*[a-z]*[ ]*[a-z]*[ ]*[a-z]*', material)
    material_list = re.findall(r'[a-z]{3,}', material)
    for ele in material_list:
        ele = ele.strip().strip('%').strip().strip(',').strip()
        
        if len(ele) > 2:
            allList.append(ele)
             
            if ele not in singlelist:
                singlelist.append(ele)

# for each_id in ids:
#     each_id = each_id.strip('\n')
#     material = ''
#      
#     material = selectINFObyID2(each_id).lower()
#     mlist = material.split('||')
#     for ele in mlist:
#         if 'composition' in ele:
#             material_list = re.findall(r'%[ ]*[a-z]+[ ]*[a-z]*[ ]*[a-z]*[ ]*[a-z]*', ele)
#      
#             for elematerial_list in material_list:
#                 elematerial_list = elematerial_list.strip().strip('%').strip().strip(',').strip()
#                 if len(elematerial_list) > 2:
#                     allList.append(elematerial_list)
#                      
#                     if elematerial_list not in singlelist:
#                         singlelist.append(elematerial_list)

for ele in singlelist:
    with open('C:/Users/Administrator/Desktop/results.txt','a', encoding='utf8') as f:
        f.write(ele + '\t' + str(allList.count(ele)) + '\n')
#     
    
#     output = infoList[allproductsList.index(wrong)].lower().strip('\n').strip('/')
#     output1 = output.split('\t')[1].split('/')[-1]
#     if 'passport' in output:
#         with open('C:/Users/Administrator/Desktop/wrongoutput.txt','a', encoding='utf8') as f:
#             from _ast import Str
#             f.write(wrong + '\n')
