#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2016年12月2日

@author: Administrator
'''

import MyFunctions_productRecategorize as MF
def extractCategoryKeywords(cKeywords):
    lst_cate = []
    lst_keywords = []
    for ele in cKeywords:
        ele = ele.strip('\n').lower()
        ele_list = ele.split(';')
        lst_cate.append(ele_list[0])
        lst_keywords.append(MF.del_null_in_list(ele_list))
        
    return lst_cate, lst_keywords

def findFeatureList(cate, productKeywords, cKeywords):
    resultList = []
    lst_cate, lst_keywords = extractCategoryKeywords(cKeywords)
    if cate != '' and ';' not in cate:
        iNumber = lst_cate.index(cate)
        keywordList = lst_keywords[iNumber]
        
        for ele in keywordList:
            if ele in productKeywords:
                if ele not in resultList:
                    resultList.append(ele)
    return resultList

cKeywords = open("C:/Users/Administrator/Desktop/tesproductRecategoryinput F_tracy20161203.txt").readlines()
# cKeywords = open("C:/Users/Administrator/Desktop/tesproductRecategoryinput F_tracy20161203.txt").readlines()
pKeywords = open("C:/Users/Administrator/Desktop/input.txt", encoding='utf8').readlines()

for ele_pKeywords in pKeywords:
    ele_pKeywords = ele_pKeywords.strip('\n').strip('\ufeff').lower()
    
    if '\t' in ele_pKeywords:
        ele_pKeywordsList = ele_pKeywords.split('\t')
        
        productID = ele_pKeywordsList[0]
        productKeywords1 = ele_pKeywordsList[1]
        productKeywords2 = ele_pKeywordsList[2]
        productKeywords = productKeywords1 + ' ' + productKeywords2
        cate = ele_pKeywordsList[3]
        
#         print(productKeywordsList)
        outputList = findFeatureList(cate, productKeywords, cKeywords)
        
        with open('C:/Users/Administrator/Desktop/output.txt','a', encoding='utf8') as f:
            f.write(productID + '\t' + MF.list_to_string(MF.del_list_duplicates(outputList)) + '\n')
