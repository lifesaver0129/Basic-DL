#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 2016年11月24日
ZW's Functions
@author: Administrator
'''
import nltk
import pymysql
from numpy import sum
import re

###########
#Input: a list
#Output: a list without duplicated elements
###########
#Start of the function
def del_list_duplicates(inputList):
    output_list = []
    if inputList is not None:
        for ele_input_list in inputList:
            if ele_input_list not in output_list:
                output_list.append(ele_input_list)
    return output_list
#End of the function
#************************************************************

###########
#Input: a string separated by ;
#Output: a list without duplicated elements
###########
#Start of the function
def del_string_duplicates(inputString):
    output_list = ''
    inputStringList = []
    if inputString != '':
        inputStringList = inputString.split(';')
        inputStringList = del_list_duplicates(inputStringList)
        inputStringList = del_null_in_list(inputStringList)
    output_list = list_to_string(inputStringList)
    return output_list
#End of the function
#************************************************************

###########
#Input: a list
#Output: a list without null elements
###########
#Start of the function
def del_null_in_list(inputList):
    output_List = []
    if inputList is not None:
        for ele_input_list in inputList:
            if len(ele_input_list) > 0:
                output_List.append(ele_input_list)
    return output_List
#End of the function
#************************************************************

###########
#Input: a string
#Output: list of all noun words in the string, may exists duplicated.
###########
#Start of the function
def extract_nouns_from_string(inputString):
    outputList = []
    if inputString is None:
        return ''
    else:
        tokens = nltk.word_tokenize(inputString)
        tagged = nltk.pos_tag(tokens)
        outputList = [word for word,pos in tagged \
            if (pos == 'NN' or pos == 'NNP' or pos == 'NNS' or pos == 'NNPS')]
    return outputList
#End of the function
#************************************************************

###########
#Input: a list
#Output: a string with each element separated by ';'.
###########
#Start of the function
def list_to_string(inputList):
    outputString = ''
    if inputList is not None:
        outputString = ';'.join(inputList)
    return outputString.strip(';')
#End of the function
#************************************************************

###########
#Input: a string; the sperator string that seperate the string, exaple: ';'
#Output: a list.
###########
#Start of the function
def string_to_list(inputString, seperator):
    outputList = []
    if inputString is not None:
        inputString = inputString.strip().strip('\n')
        list_split = inputString.split(seperator)
        for ele_list_split in list_split:
            outputList.append(ele_list_split.strip())
    return outputList
#End of the function
#************************************************************

###########
#Input: database connection; input parameter list
#Output: a string with each element separated by ';'.
###########
#Start of the function
def select_single_info(cursor, sqlString, inputData):
    cursor.execute(sqlString, inputData)
    
    fetch_result = cursor.fetchone()
    if fetch_result is not None:
        return fetch_result[0]
    else:
        return None
#************************************************************

###########
#Input: database connection; input parameter list
#Output: a string with each element separated by ';'.
###########
#Start of the function
def select_multi_info(cursor, sqlString, inputData):
    outputList = []
    cursor.execute(sqlString, inputData)
    fetch_result = cursor.fetchall()

    if fetch_result is not None:
        for ele_fetch_result in fetch_result:
            if ele_fetch_result is not None:
                outputList.append(ele_fetch_result[0])
                
    return outputList
#************************************************************

###########
#Input: database connection; input productID
#Output: a string with each element separated by ';'.
###########
#Start of the function
def delet_by_id(cursor, inputID):
    sql = 'DELETE FROM testdb.product WHERE idproduct = %s'
    cursor.execute(sql, inputID)
    db.commit()#需要这一句才能保存到数据库中
#************************************************************

###########
#Input: database connection; input productID
#Output: a string with each element separated by ';'.
###########
#Start of the function
def update_by_id(cursor, inputID, updateContent):
    sql = 'update product set product_breadcrumbs = %s where idproduct = %s'
    data = (str(updateContent), int(inputID))
    
    cursor.execute(sql, data)
    db.commit()#需要这一句才能保存到数据库中
#************************************************************

###########
#Input: two list
#Output: Union list of the two lists
###########
#Start of the function
def list_union(inputList1, inputList2):
    return list(set(inputList1).union(set(inputList2)))
#************************************************************

###########
#Input: two list
#Output: Intersection list of the two lists
###########
#Start of the function
def list_intersection(inputList1, inputList2):
    return list(set(inputList1).intersection(set(inputList2)))
#************************************************************

###########
#Input: list filtering
#Output: del list elements len < 2
###########
#Start of the function
def list_filtering(inputList):
    outputList = []
    for ele_inputList in inputList:
        if len(ele_inputList) > 1:
            outputList.append(ele_inputList)
    return outputList
#************************************************************


###########
#Input: the code of the product category
#Output: a list of matching matchcategorycode and score
###########
#Start of the function
def find_match_category_list(inputProductcode):
    outputListCode = []
    outputListScore = []
    inputProductcode = inputProductcode.strip('\ufeff')
    sql = 'SELECT matchcategorycode, score from mix_match_pairs where categorycode = %s order by score desc'
    resultList = select_multi_info(cursor, inputProductcode.strip(), sql)
    if resultList is not None:
        for ele_resultList in resultList:
            outputListCode.append(ele_resultList[0])
            outputListScore.append(ele_resultList[1])
    return outputListCode, outputListScore
#************************************************************

###########
#translate string '0' to 0
#Input: a list of strings
#Output: a list of numbsers
###########
#Start of the function
def trans_stringlist_to_intlist(inputList):
    outputList = []
    for ele in inputList:
        try:
            outputList.append(int(ele))
        except ValueError:
            outputList.append(float(ele))
    return outputList
#************************************************************

###########
#assign matching number of products since the mix match number is 10
#Input: a list of matching matchcategorycode and score
#Output: a list number of matching products
###########
#Start of the function
def assign_matching_products(inputListScore):
    outputList = []
    sumScore = sum(inputListScore)
    for iNumber in range(len(inputListScore)):
        categoryNumber = inputListScore[iNumber]*(10/sumScore)
        outputList.append(int(round(categoryNumber)))
    return outputList
#************************************************************

###########
#select all the product from database by category info.
#Input: category name or category code
#Output: a list products
###########
#Start of the function
def select_productList_by_category(cursor, categoryCode):
    outputList = []
    sql = 'select idproduct from product where product_breadcrumbs = %s'
    outputList = select_multi_info(cursor, categoryCode, sql)
    return outputList
#************************************************************

###########
#given a list of price, set two values to seperated the list into 3 parts
#Input: a list of price (numbers)
#Output: two values, level_high, level_low
###########
#Start of the function
def set_price_level(cursor, listOfProductPrice):
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
    
#************************************************************

if __name__ == '__main__':
#this is the main function.
    db = pymysql.connect("localhost","root","123456","testdb", charset="utf8")
    cursor = db.cursor()
