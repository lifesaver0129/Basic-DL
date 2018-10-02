#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 2016年11月28日

@author: Administrator
'''

import nltk
import pymysql
import string
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
#Output: all noun words in the string, may exists duplicated.
###########
#Start of the function
def extract_nouns_from_string(inputString):
    outputString = ''
    if inputString is None:
        return ''
    else:
        tokens = nltk.word_tokenize(inputString)
        tagged = nltk.pos_tag(tokens)
        outputString = [word for word,pos in tagged \
            if (pos == 'NN' or pos == 'NNP' or pos == 'NNS' or pos == 'NNPS')]
    return outputString
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
    if inputString == '':
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
        return None
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
        if len(ele_inputList) > 2:
            outputList.append(ele_inputList)
    return outputList
#************************************************************


###########
#Input: two lists, one is the productInfo list, another is the keyword list
#Output: del list elements len < 2
###########
#Start of the function
def recategorize(productInfoList, keywordList):
    outputList = []#output list
    productInfoList = del_null_in_list(productInfoList)#del null elements in list
    keywordList = del_null_in_list(keywordList)#del null elements in list
    
    for ele_productInfoList in productInfoList:#for each row of the productInfo txt file
        hitlist = []# hit category list
        ele_productInfoList = ele_productInfoList.strip('\n')#strip the '\n' of each row
        if '\t' in ele_productInfoList:
            list_ele_productInfoList = ele_productInfoList.split('\t')#split each row into list with '\t'
            
            productID = list_ele_productInfoList[0]#this is the productId of each product
            productContent = list_ele_productInfoList[1].lower()#this is productContent of each product
            list_productContent = productContent.split(';')#split each product content into a list
            list_productContent = del_null_in_list(list_productContent)##del null elements in list
            
            for ele_list_productContent in list_productContent:#for each element in product list
                for ele_keywordList in keywordList:#for each row in the keyword file
                    ele_keywordList = ele_keywordList.strip('\n')#strip '\n' in each row
                    ele_keywordList = ele_keywordList.lower()#change each row in to lower character
                    list_ele_keywordList = ele_keywordList.split(';')#split the keyword string into a string
                    list_ele_keywordList = del_null_in_list(list_ele_keywordList)##del null elements in list
                    
                    cate = list_ele_keywordList[0]# the first element is the category name of each row
                    for ele_list_ele_keywordList in list_ele_keywordList:#for each element in each row, if a word in the list
                        if ele_list_productContent == ele_list_ele_keywordList:
                            hitlist.append(cate)#store the category name                        
            data = [productID, list_to_string(hitlist)]#productID and hitlist
            outputList.append(data)#append to the output list
    return outputList
#************************************************************

def recategorize_1(productIDList, productInfoList, keywordList):
    outputList = []#output list
    for productInfoList_number in range(len(productInfoList)):
        hitlist = []# hit category list
        productID = productIDList[productInfoList_number]#this is the productId of each product
        productContent = productInfoList[productInfoList_number].strip('\n')#strip the '\n' of each row
        
        list_productContent = productContent.split(';')#split each product content into a list
        list_productContent = del_null_in_list(list_productContent)##del null elements in list
        
        for ele_list_productContent in list_productContent:#for each element in product list
            #for ele_keywordList in keywordList:#for each row in the keyword file
            for ele_keywordList in keywordList[2:]:#for each row in the keyword file
                ele_keywordList = ele_keywordList.strip('\n')#strip '\n' in each row
                ele_keywordList = ele_keywordList.lower()#change each row in to lower character
                list_ele_keywordList = ele_keywordList.split(';')#split the keyword string into a string
                list_ele_keywordList = del_null_in_list(list_ele_keywordList)##del null elements in list
                
                cate = list_ele_keywordList[0]# the first element is the category name of each row
                for ele_list_ele_keywordList in list_ele_keywordList:#for each element in each row, if a word in the list
                    if ele_list_productContent == ele_list_ele_keywordList:
                        hitlist.append(cate)#store the category name                        
        data = [productID, list_to_string(hitlist)]#productID and hitlist
        outputList.append(data)#append to the output list
    return outputList

#recategorize
def recategorize_2(inputContent, inputKeywords):
    productIDList = []
    productContentList = []
    for ele_inputContent in inputContent:
        ele_inputContent = ele_inputContent.strip('\n')
        
        if '\t' in ele_inputContent:
            list_ele_inputContent = ele_inputContent.split('\t')
            productID = list_ele_inputContent[0]
            productContent = list_ele_inputContent[1]
            
            productIDList.append(productID)
            productContentList.append(productContent)

    with open('C:/Users/Administrator/Desktop/output.txt','a', encoding='utf8') as f:
        for ele in recategorize_1(productIDList, productContentList, inputKeywords):
            f.write(ele[0] + '\t' + ele[1] + '\n')
            
            
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

###########
#Input: Read the txt file into lists
#Output: 5 lists
###########
#Start of the function
def readTXT(inputTxtPath):
    content = open(inputTxtPath, encoding='utf8').readlines()
    list_productID = []
    list_title = []
    list_desc = []
    list_bread = []
    
    for ele_content in content:
        ele_content = ele_content.strip('\n').lower()
        if '\t' in ele_content:
            list_ele_content = ele_content.split('\t')
      
            productID = list_ele_content[0].strip()
            productTitle = list_ele_content[1].replace('&', ' ').replace(';',' ').replace(':',' ').strip()
            productDescription = list_ele_content[2].replace('&', ' ').replace(';',' ').replace(':',' ').replace('.',' ').strip()
            productBreadcrumbs = list_ele_content[3].replace('&', ' ').replace('/', ' ').replace(':',' ').replace(';',' ').strip()
            
            list_bread.append(productBreadcrumbs.split())
            list_title.append(productTitle.split())
            list_desc.append(productDescription.split())
            
            list_productID.append(productID)
        
    return list_productID, list_title, list_desc, list_bread

#************************************************************

###########
#Input: hitlist
#Output: hitlist
###########
#Start of the function
def hitlist_decision(inputTxtFilePath):
    txtFile = open(inputTxtFilePath, encoding='utf8').readlines()
    list_priority_1 = []
    list_priority_2 = []
    list_priority_3 = []
    list_priority_4 = []
    list_priority_5 = []
    list_priority_6 = []
    list_priority_7 = []
    list_priority_8 = []
    for ele_txtFile in txtFile:
        ele_txtFile = ele_txtFile.strip('\n')
        if '\t' in ele_txtFile:
            list_ele_txtFile = ele_txtFile.split('\t')
      
            list_priority_1.append(list_ele_txtFile[0])
            list_priority_2.append(list_ele_txtFile[1])
            list_priority_3.append(list_ele_txtFile[2])
            list_priority_4.append(list_ele_txtFile[3])
            list_priority_5.append(list_ele_txtFile[4])
            list_priority_6.append(list_ele_txtFile[5])
            list_priority_7.append(list_ele_txtFile[6])
            list_priority_8.append(list_ele_txtFile[7])
    
    hitlist = list_priority_1
    
    i = 0
    while i < len(hitlist):
        if hitlist[i] == '' and list_priority_2[i] != '':
            hitlist[i] = list_priority_2[i]
        i = i + 1

    i = 0
    while i < len(hitlist):
        if hitlist[i] == '' and list_priority_3[i] != '':
            hitlist[i] = list_priority_3[i]
        i = i + 1

    i = 0
    while i < len(hitlist):
        if hitlist[i] == '' and list_priority_4[i] != '':
            hitlist[i] = list_priority_4[i]
        i = i + 1

    i = 0
    while i < len(hitlist):
        if hitlist[i] == '' and list_priority_5[i] != '':
            hitlist[i] = list_priority_5[i]
        i = i + 1
        
    i = 0
    while i < len(hitlist):
        if hitlist[i] == '' and list_priority_6[i] != '':
            hitlist[i] = list_priority_6[i]
        i = i + 1

    i = 0
    while i < len(hitlist):
        if hitlist[i] == '' and list_priority_7[i] != '':
            hitlist[i] = list_priority_7[i]
        i = i + 1
        
    i = 0
    while i < len(hitlist):
        if hitlist[i] == '' and list_priority_8[i] != '':
            hitlist[i] = list_priority_8[i]
        i = i + 1

    return hitlist



if __name__ == '__main__':
#this is the main function.
    db = pymysql.connect("localhost","root","123456","testdb", charset="utf8")
#     db = pymysql.connect("158.132.123.119","root","tozmartdev2016","b2c-zw", 13306, charset="utf8")
    # 使用cursor()方法获取操作游标 
    cursor = db.cursor()
    
    cateKeywords = open("C:/Users/Administrator/Desktop/productRecategory/W input _tracy20161129.txt").readlines()
    productContent = open("C:/Users/Administrator/Desktop/input.txt", encoding='utf8').readlines()
    #read the product info into lists
    list_productID, \
    list_title, \
    list_desc, \
    list_bread = readTXT("C:/Users/Administrator/Desktop/input.txt")
    
    list_productID = list_productID
    list_1_intersection = []
    list_2_intersection = []
    list_3_intersection = []
    list_4_intersection = []
    list_5_1_intersection = []
    list_5_2_intersection = []
    list_6_1_intersection = []
    list_6_2_intersection = []
    
    testlist = []
    for i_number in range(len(list_productID)):
        productID = list_productID[i_number]
        product_title = list_title[i_number]
        product_desc = list_desc[i_number]
        product_bread = list_bread[i_number]
         
        intersection_1 = list_intersection(list_intersection(product_bread, product_title), product_desc)
        intersection_2 = list_intersection(product_title, product_desc)
        intersection_3 = list_intersection(product_title, product_bread)
        intersection_4 = list_intersection(product_desc, product_bread)
        
        intersection_5_1 = product_title
        intersection_5_2 = product_bread
     
        intersection_6_1 = product_desc
        intersection_6_2 = product_bread
         
        list_1_intersection.append(list_to_string(del_null_in_list(intersection_1)))
        list_2_intersection.append(list_to_string(del_null_in_list(intersection_2)))
        list_3_intersection.append(list_to_string(del_null_in_list(intersection_3)))
        list_4_intersection.append(list_to_string(del_null_in_list(intersection_4)))
        list_5_1_intersection.append(list_to_string(del_null_in_list(intersection_5_1)))
        list_5_2_intersection.append(list_to_string(del_null_in_list(intersection_5_2)))
        list_6_1_intersection.append(list_to_string(del_null_in_list(intersection_6_1)))
        list_6_2_intersection.append(list_to_string(del_null_in_list(intersection_6_2)))

    for indexNumber in range(len(list_productID)):
        with open('C:/Users/Administrator/Desktop/output_1.txt','a', encoding='utf8') as f:
            f.write(list_productID[indexNumber] + '\t' + \
                    list_1_intersection[indexNumber] +'\t' + \
                    list_2_intersection[indexNumber] +'\t' + \
                    list_3_intersection[indexNumber] +'\t' + \
                    list_4_intersection[indexNumber] +'\t' + \
                    list_5_1_intersection[indexNumber] +'\t' + \
                    list_5_2_intersection[indexNumber] +'\t' + \
                    list_6_1_intersection[indexNumber] +'\t' + \
                    list_6_2_intersection[indexNumber] +'\t' + '\n')




