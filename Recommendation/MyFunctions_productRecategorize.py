#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 2016年11月24日
ZW's Functions
@author: Administrator
'''
import nltk, re
import pymysql

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
#Input: a list
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
            if ele_input_list != '':
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
        for ele in inputList:
            outputString = outputString + str(ele) + ';'
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
    if inputString == '' or inputString is None:
        return []
    else:
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
def find_single_info_by_id(cursor, inputID):
    sql = 'select product_sku from testdb.product where idproduct = %s'
    cursor.execute(sql, id)
    
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
def find_multi_info_by_id(cursor, inputID):
    outputList = []
    sql = 'select product_sku from testdb.product where idproduct = %s'
    cursor.execute(sql, id)
    
    fetch_result = cursor.fetchall()
    if fetch_result is not None:
        for ele_fetch_result in fetch_result:
            if ele_fetch_result is not None:
                outputList.append(ele_fetch_result)
        return outputList
    else:
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
#Input: two lists, one is the productInfo list, another is the keyword list
#Output: del list elements len < 2
def recategorize(list_product_column, category_list, keyword_list):
    resultList = []
    
    for iNumber in range(len(list_product_column)):
        categoryString = ''
        line_product_content = list_product_column[iNumber]
        for ele_keyword_list in keyword_list:
            ele_keyword_list = del_null_in_list(ele_keyword_list)
            
            for ele_ele_keyword_list in ele_keyword_list:
                if ele_ele_keyword_list in line_product_content:
                    
                    categoryString = categoryString + ';' + category_list[keyword_list.index(ele_keyword_list)]
                    categoryString = categoryString.strip(';')
        resultList.append(categoryString)
    return resultList
#************************************************************


def recategorize2(columnTitle, columnBreadcrumbs, columnDesc):
    outputstring = []
    
    for iNumber in range(len(columnTitle)):
        #如果columnTitle不为空，则选title决定的category
        newcategory = ''
        if columnTitle[iNumber] != '' and columnBreadcrumbs[iNumber] != '':
            if len(list(set(columnTitle[iNumber].split(';'))&(set(columnBreadcrumbs[iNumber].split(';'))))) > 0:
                newcategory = list_to_string(list(set(columnTitle[iNumber].split(';'))&(set(columnBreadcrumbs[iNumber].split(';')))))
                outputstring.append(newcategory)
                continue
        if columnTitle[iNumber] != '':
            newcategory = columnTitle[iNumber]
            outputstring.append(newcategory)
            continue
        if columnBreadcrumbs[iNumber] != '':
            newcategory = columnBreadcrumbs[iNumber]
            outputstring.append(newcategory)
            continue
        if columnDesc[iNumber] != '':
            newcategory = columnDesc[iNumber]
            outputstring.append(newcategory)
            continue
        else:
            outputstring.append('')
    return outputstring


###########
#Input: Find the most element in the list
#Output: the most frequence element in the list
###########
#Start of the function
def sortbylistcount(inputList):
    countNubmer = 0
    outputResult = ''
    for ele_inputList in inputList:
        if len(ele_inputList) > 0:
            if inputList.count(ele_inputList) > countNubmer:
                outputResult = ele_inputList
                countNubmer = inputList.count(ele_inputList)
    return outputResult
#************************************************************

#read txt file into list on list
#keywords in each line is a list; all lines is a list
#return category list and total keyword list
def readKeywordsIntoList(inputTxtPath):
    content = open(inputTxtPath, encoding='utf8').readlines()
    total_list = []
    cate_list = []
    for eachLine in content:
        eachLine = eachLine.strip('\n').lower()
        
        if len(eachLine) > 0:
            list_eachLine = eachLine.split(';')
            cate_list.append(list_eachLine[0])
            list_eachLine = del_null_in_list(list_eachLine)
            total_list.append(list_eachLine)
    return cate_list, total_list
#************************************************************

###########
#Input: Read the txt file into lists
#Output: 5 lists
###########
#Start of the function
def readProductContentIntoList(inputTxtPath):
    content = open(inputTxtPath, encoding='utf8').readlines()

    list_productID = []
    list_title_1 = []
    list_description_2 = []
    list_bread_3 = []
    
    for ele_content in content:
        ele_content = ele_content.lower().strip('\n')
        if '\t' in ele_content:
            list_ele_content = ele_content.split('\t')
      
            productID = list_ele_content[0].strip()
            list_productID.append(int(productID))
            
            title_1 = list_ele_content[1].strip()
            list_title_1.append(title_1)
            
            description_2 = list_ele_content[2].strip()
            list_description_2.append(description_2)
            
            bread_3 = list_ele_content[3].strip()
            list_bread_3.append(bread_3)
        
    return list_productID, list_title_1, list_description_2, list_bread_3
#************************************************************

def hit_decision(inputListA, inputListB):
    final_result_list = []
    
    for iNumbser in range(len(inputListA)):
        resultList = ''
        content_1 = inputListA[iNumbser]
        content_2 = inputListB[iNumbser]
        
        if content_1 == '':
            if content_2 == '':
                resultList = ''
            else:
                resultList = content_2
        else:
            if content_2 == '':
                resultList = content_1
            else:
                resultList = list_to_string(del_null_in_list(list_intersection(content_2.split(';'), content_1.split(';'))))
        final_result_list.append(resultList)
    return final_result_list

############################################
def final_decision(inputListA, inputListB):
    final_result_list = []
    
    for iNumbser in range(len(inputListA)):
        result = ''
        content_1 = inputListA[iNumbser]
        content_2 = inputListB[iNumbser]
        
        if content_1 == content_2:
            result = content_1
        else:
            combine_list = content_1.split(';') + content_2.split(';')
            combine_list = del_null_in_list(combine_list)
            result = sortbylistcount(combine_list)
        final_result_list.append(result)
    return final_result_list
############################################

if __name__ == '__main__':
#this is the main function.
    db = pymysql.connect("localhost","root","123456","testdb", charset="utf8")
#     db = pymysql.connect("158.132.123.119","root","tozmartdev2016","b2c-zw", 13306, charset="utf8")
    # 使用cursor()方法获取操作游标 
    cursor = db.cursor()
 


