#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pymysql
import MyFunctions as MF


def num(s):
    try:
        return int(s)
    except ValueError:
        return float(s)



product_category = open("C:/Users/Administrator/Desktop/category_id_name_code_gender.txt")
mix_matrix = open("C:/Users/Administrator/Desktop/category_matrixM.txt")


list_categoryName = []
list_categoryCode = []

for ele_product_category in product_category:
    ele_product_category = ele_product_category.strip('\n')
    line_list_product_category = ele_product_category.split('\t')
    
    list_categoryName.append(line_list_product_category[1])
    list_categoryCode.append(line_list_product_category[0])

list_matrix = []
for ele_mix_matrix in mix_matrix:
    ele_mix_matrix = ele_mix_matrix.strip('\n')
    line_list_mix_matrix = ele_mix_matrix.split('\t')
    list_matrix.append(line_list_mix_matrix)

idmatchList = []
for iNumber in range(len(list_categoryName)):
    lineList = list_matrix[iNumber]
    
    for iNumber2 in range(len(lineList)):
        if lineList[iNumber2] != '0':
            nonzero = []
            nonzero = [list_categoryName[iNumber], list_categoryCode[iNumber], list_categoryName[iNumber2], list_categoryCode[iNumber2], lineList[iNumber2]]
            if nonzero not in idmatchList:
                idmatchList.append(nonzero)
for ele in idmatchList:
    with open('C:/Users/Administrator/Desktop/output.txt','a') as f:
        f.write(ele[0] + '\t' + ele[1] + '\t' + ele[2] + '\t' + ele[3] + '\t' + ele[4] + '\n')
