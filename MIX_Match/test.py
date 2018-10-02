#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re, pymysql
import MyFunctions as MF
zalora = open("C:/Users/Administrator/Desktop/input.txt", encoding='utf8').readlines()

db = pymysql.connect("localhost","root","123456","test", charset="utf8")
cursor = db.cursor()

sqlstring = 'select code from test.category where parent_name = %s and name = %s and gender = %s'

for ele in zalora:
    ele = ele.strip('\n')
    elelst = ele.split('\t')
    gender = elelst[0]
    product_name = elelst[1]
    
    product_featureList = re.findall(r':[a-z A-Z]+;', elelst[2])
    product_featureList2 = []
    for ele in product_featureList:
        ele = ele.strip(';').strip(':').strip()
        product_featureList2.append(ele)
    
    codelist = []
    
    if len(product_name) > 0:
        if len(product_featureList2) > 0:
            for ele in product_featureList2:
                code = '****'
                data = (product_name, ele.strip(), gender)
                cursor.execute(sqlstring, data)
                fetch_result = cursor.fetchone()
                if fetch_result is not None:
                    code = fetch_result[0]
                else:                    
                    print(product_name + '\t' + ele)
                codelist.append(code)
    with open('C:/Users/Administrator/Desktop/output.txt','a', encoding='utf8') as f:
        f.write(product_name + '\t' + elelst[2] + '\t' + MF.list_to_string(codelist) + '\n')
