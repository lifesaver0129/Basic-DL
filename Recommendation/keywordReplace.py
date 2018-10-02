#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2016年12月3日

@author: Administrator
'''

import MyFunctions_productRecategorize as MF
pKeywords = open("C:/Users/Administrator/Desktop/input.txt", encoding='utf8').readlines()

cate_list, total_list = MF.readKeywordsIntoList("C:/Users/Administrator/Desktop/tesproductRecategoryngular_pural_20161203.txt")

for iNumber in range(len(pKeywords)):
    ele_pKeywords = pKeywords[iNumber].lower().strip()
    ele_pKeywordsList = ele_pKeywords.split(';')
    ele_pKeywordsList = MF.del_list_duplicates(ele_pKeywordsList)
    
    resultOutput = ele_pKeywordsList

    for inumber2 in range(len(ele_pKeywordsList)):
        for ele_total_list in total_list:
            if ele_pKeywordsList[inumber2] in ele_total_list:
                resultOutput[inumber2] = cate_list[total_list.index(ele_total_list)]
    
    with open('C:/Users/Administrator/Desktop/output.txt','a', encoding='utf8') as f:
        f.write(MF.list_to_string(MF.del_list_duplicates(resultOutput)) + '\n')
