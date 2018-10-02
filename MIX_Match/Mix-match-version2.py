#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2017年1月10日
@author: Administrator
'''

import MyFunctions as MF
import pymysql, nltk
import re, random
import numpy as np

def find_product_info(target_productID):
    outputList = []
    sqlString = "SELECT * FROM clean_data_zalora.product where idproduct = %s"

    cursor.execute(sqlString, target_productID)
    fetch_result = cursor.fetchone()

    if fetch_result is not None:
        for ele_fetch_result in fetch_result:
            outputList.append(ele_fetch_result)
    return outputList

def find_category_level_match(target_product_category):
    category_with_no_2nd_lvl_matchList = []
    category_with_no_2nd_lvl_matchList_scoreList = []

    category_with_2nd_lvl_matchList = []
    category_with_2nd_lvl_matchList_scoreList = []

    sqlString = 'SELECT matchcategorycode, score FROM clean_data_zalora.mix_match_pairs where categorycode = %s and level = %s'
    cursor.execute(sqlString, (target_product_category, '1')) # first level category match
    fetch_result = cursor.fetchall()

    if fetch_result is not None:
        for ele_fetch_result in fetch_result:
            if float(ele_fetch_result[1]) > 1:# category match with 2nd(feature) level
                category_with_2nd_lvl_matchList.append(ele_fetch_result[0])
                category_with_2nd_lvl_matchList_scoreList.append(ele_fetch_result[1])
            else:
                category_with_no_2nd_lvl_matchList.append(ele_fetch_result[0])
                category_with_no_2nd_lvl_matchList_scoreList.append(ele_fetch_result[1])
    return category_with_no_2nd_lvl_matchList, category_with_no_2nd_lvl_matchList_scoreList, \
        category_with_2nd_lvl_matchList, category_with_2nd_lvl_matchList_scoreList


def find_features_match_the_category(categoryName):
    featureList = []
    
    sqlString = "select matchcategorycode FROM clean_data_zalora.mix_match_pairs where categorycode = %s and level = %s and matchcategorycode like %s"

    cursor.execute(sqlString, (categoryName, '2', '%F%')) # first level category match
    fetch_result = cursor.fetchall()

    if fetch_result is not None:
        for ele_fetch_result in fetch_result:
            featureList.append(ele_fetch_result[0])
    return featureList

def find_feature_level_match(target_product_featureList):
    matchcategoryList = []
    scorelist = []
    
    if len(target_product_featureList) > 0:
        for ele in target_product_featureList:
            sqlString = 'SELECT matchcategorycode, score from clean_data_zalora.mix_match_pairs where categorycode = %s and matchcategorycode like %s'
            cursor.execute(sqlString, (ele, '%F%'))
            fetch_result = cursor.fetchall()

            if fetch_result is not None:
                for ele_fetch_result in fetch_result:
                    matchcategoryList.append(ele_fetch_result[0])
                    scorelist.append(float(ele_fetch_result[1]))
    return matchcategoryList, scorelist


def find_products_with_featureLevel(categoryCode, featureList_match_the_category):
    productList = []
    
    if len(featureList_match_the_category) > 0:
        for ele_featureList_match_the_category in featureList_match_the_category:
            sqlString = "SELECT idproduct from clean_data_zalora.product where category = %s and feature like %s"
            cursor.execute(sqlString, (categoryCode, '%' + ele_featureList_match_the_category + '%'))
            fetch_result = cursor.fetchall()
        
            if fetch_result is not None:
                for ele_fetch_result in fetch_result:
                    productList.append(ele_fetch_result[0])
    return productList

def find_products_with_no_featureLevel(categorylevelcode):
    outputList = []
    
    sqlString = "SELECT idproduct from clean_data_zalora.product where category = %s and feature = ''"
    cursor.execute(sqlString, categorylevelcode)
    fetch_result = cursor.fetchall()

    if fetch_result is not None:
        for ele_fetch_result in fetch_result:
            outputList.append(ele_fetch_result[0])
    return outputList

def find_parent_category(featureList):
    outputList = []
    
    for ele in featureList:
        sqlString = 'SELECT parent_code FROM test.category where code = %s'
        cursor.execute(sqlString, ele)
        fetch_result = cursor.fetchone()

        if fetch_result is not None:
            for ele_fetch_result in fetch_result:
                if ele_fetch_result not in outputList:
                    outputList.append(ele_fetch_result)
    return outputList

def calculate_product_match_score(target_productInfoList, category_match_product_poolList, feature_matchList, feature_scoreList):
    product_matchList = []
    for i in range(len(category_match_product_poolList)):
        ele_category_scoreList = []
        ele_category_scoreList = calculate_match_score_in_each_category(target_productInfoList, category_match_product_poolList[i], feature_matchList, feature_scoreList)
        product_matchList.append(ele_category_scoreList)
    return product_matchList

def calculate_match_score_in_each_category(target_productInfoList, product_list, feature_matchList, feature_scoreList):
    match_score_in_category = []
    templist = []
    for ele in product_list:
        matchScore = calculate_match_score_for_each_product(target_productInfoList, ele, feature_matchList, feature_scoreList)
        templist.append(matchScore)
#     templist.sort(reverse=True)
#     print(templist)
    
    # sorting the indices of the templist in reverse way.
    indiceList = [i[0] for i in sorted(enumerate(templist), key=lambda x:x[1])][::-1]
     
    for ele in indiceList:
        temp = product_list[ele]
        match_score_in_category.append(temp)
    return match_score_in_category

def calculate_match_score_for_each_product(target_productInfoList, productID, feature_matchList, feature_scoreList):
    final_score = 0

    brand_score = 0
    price_score = 0
    color_score = 0
    feature_match_score = 0

    match_product_info = find_product_info(productID) 
    # sequence is idproduct, breadcrumbs, title, brand, gender, price, description, colour, category, feature
    
    if target_productInfoList[3] == match_product_info[3]:
        brand_score = 1
        
    if colour_similarity(target_productInfoList[7], match_product_info[7]) == 1:
        color_score = 1

    if float(match_product_info[5]) > float(target_productInfoList[5])*0.8 and float(match_product_info[5]) < float(target_productInfoList[5])*1.2:
        price_score = 1 - abs(float(match_product_info[5]) - float(target_productInfoList[5]))/float(target_productInfoList[5])
    
    if len(feature_matchList) > 0:
        match_product_featureList = match_product_info[9].split(';')
        if len(MF.list_intersection(feature_matchList, match_product_featureList)) > 0:
            scorelist = []
            for iNumber in range(len(feature_matchList)):
                if feature_matchList[iNumber] in match_product_featureList:
                    scorelist.append(feature_scoreList[iNumber])
            feature_match_score = sum(scorelist)/len(MF.list_intersection(feature_matchList, match_product_featureList))
        final_score = (brand_score*0.5 + price_score*0.3 + color_score*0.2)*feature_match_score
    else:
        final_score = brand_score*0.5 + price_score*0.3 + color_score*0.2
        
    return final_score

def query_colour_type_num_by_colour(product_colour):
    outputInt = 0
    if len(product_colour) > 0:
        sql_query_colour_type_num_by_colour = "SELECT type_number FROM clean_data_zalora.colour where description = %s"
        cursor.execute(sql_query_colour_type_num_by_colour, product_colour)
        query_colour_type_num_by_colour_result = cursor.fetchone()
        
        if query_colour_type_num_by_colour_result is not None:
            outputInt = query_colour_type_num_by_colour_result[0]
    return outputInt

def colour_similarity(colour_1, colour_2):
    colour_1_type = query_colour_type_num_by_colour(colour_1)
    colour_2_type = query_colour_type_num_by_colour(colour_2)

    if colour_1_type == 0 or colour_2_type == 0 or colour_1_type == 11 or colour_2_type == 11:
        return 0
    else:
        if colour_1_type == colour_2_type:
            return 1
        else:
            return 0


def select_match_from_pool(idices, poolList, outputList):
    for eleList in poolList:
        if len(outputList) == 10:
            return outputList
        if len(eleList) > idices:
            if eleList[idices] > 0:# only choose these products that score greater than 0
                outputList.append(eleList[idices])
    return outputList

#this is the main function
if __name__ == '__main__':
    # this is the main function.
    db = pymysql.connect(host="localhost",
                         user="root",
                         password="123456",
                         db="clean_data_zalora",
                         charset="utf8")
    cursor = db.cursor()
    zaloraProducts = open("C:/Users/Administrator/Desktop/new_zalora_id.txt", encoding='utf8').readlines()

    for ele_zaloraProducts in zaloraProducts:# Define, Call this productID as target product.
        recNumber = 10
        final_matchList = []  # the final result

        # define the parameters.
        target_productID = ele_zaloraProducts.strip('\n')  # the product ID of the target product.
#         target_productID = 52165
        print(target_productID)
        
        # find target_product_category, target_product_featureList and gender from category_mapping Table.
        target_productInfoList = find_product_info(target_productID)
        target_product_category = target_productInfoList[8]
        target_product_featureList = target_productInfoList[9].split(';') # given a product, features selected under the category.
        target_product_gender = target_productInfoList[4]
        
        category_matchList = [] # the match list of the product category.
        category_scoreList = [] # the score of the match category with the target product
#         category_numberList = [] # the number of products assigned to each match category.

        category_match_product_poolList = [] # list on list
        category_match_pool = [] # the candidate products in category level.

        feature_matchList = [] # the match list of the product feature.
        feature_scoreList = [] # the score of the match feature with the target product

        category_no_branch = [] # subbranch of category, there is no feature matches in the category.
        category_with_branch = [] # subbranch of category, there are feature matches in the category.

        ele_category_match_productList = [] # the match products in category level.
        ele_feature_match_productList = [] # the match products in feature level.

        # find category level match
        if target_product_category == '': # there is no match in category level, no match in the last.
            print('There is no matching product. target_productID: ', target_productID)
            continue  #跳出此次for循环
        
        category_with_no_2nd_lvl_matchList, category_with_no_2nd_lvl_matchList_scoreList, \
        category_with_2nd_lvl_matchList, category_with_2nd_lvl_matchList_scoreList = find_category_level_match(target_product_category)
        
        # calculate the poollist of category_with_no_2nd_lvl_matchList
        if len(category_with_no_2nd_lvl_matchList) > 0: # the category_with_no_2nd_lvl_matchList is not null, exits at least one match category.
            for ele_category_matchList in category_with_no_2nd_lvl_matchList: #find products pool in each match category.
                ele_match_productList = []
                ele_match_productList = find_products_with_no_featureLevel(ele_category_matchList)
                category_match_product_poolList.append(ele_match_productList)
        else:# there is no match in category_with_no_2nd_lvl_matchList.
            print('There is no category_with_no_2nd_lvl_matchList. target_productID: ', target_productID)
        
        # calculate the poollist of category_with_2nd_lvl_matchList
        if len(category_with_2nd_lvl_matchList) > 0:# the category_matchList is not null, exits at least one match category.
            # find feature level match
            if len(target_product_featureList) > 0:# the featureList of the target product is null, the score is 0
                feature_matchList, feature_scoreList = find_feature_level_match(target_product_featureList)
                if len(feature_matchList) > 0:
                    for ele_category_matchList in category_with_2nd_lvl_matchList: #find products pool in each match category.
                        ele_match_productList = []
                        ele_features_match_the_category = find_features_match_the_category(ele_category_matchList)
                        
                        ele_match_productList = find_products_with_featureLevel(ele_category_matchList, ele_features_match_the_category)
                        category_match_product_poolList.append(ele_match_productList)
        else:
            print('There is no category_with_2nd_lvl_matchList. target_productID: ', target_productID)

        category_match_score_poolList = calculate_product_match_score(target_productInfoList, category_match_product_poolList, feature_matchList, feature_scoreList)
        category_match_score_poolList = MF.del_null_in_list(category_match_score_poolList)
         
        idicis = 0
        while len(final_matchList) < recNumber:
            final_matchList = select_match_from_pool(idicis, category_match_score_poolList, final_matchList)
            idicis = idicis + 1

        with open('C:/Users/Administrator/Desktop/output.txt','a', encoding='utf8') as f:
            f.write(str(target_productID) + '\t' + target_product_category + '\t' + str(target_product_featureList) + '\t' + str(category_matchList) + '\t' + str(feature_matchList) + '\t' + str(final_matchList) + '\n')
    db.close()