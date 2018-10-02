#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2017年1月12日

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

def find_category_level_match(target_product_category_code):
    category_matchList = []
    category_matchList_scoreList = []

    sqlString = 'SELECT matchcategorycode, score FROM clean_data_zalora.mix_match_pairs where categorycode = %s and matchcategorycode like %s'
    cursor.execute(sqlString, (target_product_category_code, '%P%')) # first level category match
    fetch_result = cursor.fetchall()

    if fetch_result is not None:
        for ele_fetch_result in fetch_result:
            if ele_fetch_result[0] not in category_matchList:
                category_matchList.append(ele_fetch_result[0])
                category_matchList_scoreList.append(ele_fetch_result[1])

    return category_matchList, category_matchList_scoreList


def find_features_match_the_category(categoryName):
    featureList = []
    
    sqlString = "select matchcategorycode FROM clean_data_zalora.mix_match_pairs where categorycode = %s and level = %s and matchcategorycode like %s"

    cursor.execute(sqlString, (categoryName, '2', '%F%')) # first level category match
    fetch_result = cursor.fetchall()

    if fetch_result is not None:
        for ele_fetch_result in fetch_result:
            featureList.append(ele_fetch_result[0])
    return featureList

def find_feature_level_match(target_product_category):
    category_featrue_matchList = []
    category_featrue_matchList_scorelist = []
    
    sqlString = 'SELECT matchcategorycode, score from clean_data_zalora.mix_match_pairs where categorycode = %s and matchcategorycode like %s'
    cursor.execute(sqlString, (target_product_category, '%F%'))
    fetch_result = cursor.fetchall()

    if fetch_result is not None:
        for ele_fetch_result in fetch_result:
            category_featrue_matchList.append(ele_fetch_result[0])
            category_featrue_matchList_scorelist.append(float(ele_fetch_result[1]))
    return category_featrue_matchList, category_featrue_matchList_scorelist


def find_products_with_featureLevel(categoryCode, feature_under_the_category):
    productList = []
    
    if len(feature_under_the_category) > 0:
        for ele_feature_matchList in feature_under_the_category:
            sqlString = "SELECT idproduct from clean_data_zalora.product where category = %s and feature like %s"
            cursor.execute(sqlString, (categoryCode, '%'+ele_feature_matchList+'%'))
            fetch_result = cursor.fetchall()
        
            if fetch_result is not None:
                for ele_fetch_result in fetch_result:
                    if ele_fetch_result[0] not in productList:
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

def find_feature_parent(feature_matchList):
    feature_parentList = []
    for ele in feature_matchList:
        sqlString = "SELECT parent_code FROM clean_data_zalora.category where code = %s"
        cursor.execute(sqlString, ele)
        fetch_result = cursor.fetchone()

        if fetch_result is not None:
            for ele_fetch_result in fetch_result:
                if ele_fetch_result not in feature_parentList:
                    feature_parentList.append(ele_fetch_result)
    return feature_parentList

def find_children_feature_by_category_code(categoryCode):
    feature_List = []
    
    sqlString = "SELECT code FROM clean_data_zalora.category where parent_code = %s and code like %s"
    cursor.execute(sqlString, (categoryCode, '%F%'))
    fetch_result = cursor.fetchall()

    if fetch_result is not None:
        for ele_fetch_result in fetch_result:
            if ele_fetch_result not in feature_List:
                feature_List.append(ele_fetch_result[0])
    return feature_List


def calculate_product_match_score(target_productInfoList, category_match_product_poolList, feature_matchList, feature_scoreList):
    product_matchList = []
    for i in range(len(category_match_product_poolList)):
        ele_category_scoreList = []
        ele_category_scoreList = calculate_match_score_in_each_category(target_productInfoList, category_match_product_poolList[i], feature_matchList, feature_scoreList)
        product_matchList.append(ele_category_scoreList)
    return product_matchList

def calculate_match_score_in_each_category(target_productInfoList, product_list, feature_matchList, feature_scoreList):
    match_products_in_category = []
    templist = []
    if len(product_list) > 0:
        for ele_product_list in product_list:
            matchScore = calculate_match_score_for_each_product(target_productInfoList, ele_product_list, feature_matchList, feature_scoreList)
            templist.append(matchScore)
        indiceList = [i[0] for i in sorted(enumerate(templist), key=lambda x:x[1])][::-1]
    
        for ele in indiceList:
            temp = product_list[ele]
            match_products_in_category.append(temp)

        if len(match_products_in_category) > 10:
            match_products_in_category = match_products_in_category[0:10]
    return match_products_in_category

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
    if brand_score == 0 and color_score == 0:
        final_score
    mapping_price_target_product, price_level_target = find_mapping_product_price(target_productInfoList)
    mapping_price_match_product, price_level_match = find_mapping_product_price(match_product_info)
    
    if price_level_target == 0 or price_level_match == 0:
        price_score = 1 - abs(float(match_product_info[5]) - float(target_productInfoList[5]))/float(target_productInfoList[5])
    if price_level_target == price_level_match:
        if mapping_price_target_product == mapping_price_match_product:
            price_score = 1
        elif abs(mapping_price_target_product-mapping_price_match_product) == 20 or \
        abs(mapping_price_target_product-mapping_price_match_product) == 33:
            price_score = 0.5
    else:
        if abs(mapping_price_target_product-mapping_price_match_product) == 12 or \
        abs(mapping_price_target_product-mapping_price_match_product) == 6 or \
        abs(mapping_price_target_product-mapping_price_match_product) == 1:
            price_score = 1
        if abs(mapping_price_target_product-mapping_price_match_product) == 7 or \
        abs(mapping_price_target_product-mapping_price_match_product) == 26 or \
        abs(mapping_price_target_product-mapping_price_match_product) == 14:
            price_score = 0.5
    
    match_product_featureList = match_product_info[9].split(';')
    if len(list(set(match_product_featureList)&set(feature_matchList))) > 0:
        if len(MF.list_intersection(feature_matchList, match_product_featureList)) > 0:
            scorelist = []
            for iNumber in range(len(feature_matchList)):
                if feature_matchList[iNumber] in match_product_featureList:
                    scorelist.append(feature_scoreList[iNumber])
            feature_match_score = sum(scorelist)/len(match_product_featureList)
        final_score = (brand_score*0.5 + price_score*0.3 + color_score*0.2)*feature_match_score
    else:
        final_score = brand_score*0.5 + price_score*0.3 + color_score*0.2
    return final_score

def find_mapping_product_price(productInfo):
    mapping_price = 0
    priceList = []
    p_price = float(productInfo[5])
    p_category_code = productInfo[8]
    
    sqlstring = 'select category_price_level from clean_data_zalora.category where code = %s'
    cursor.execute(sqlstring, p_category_code)
    fetch_result = cursor.fetchone()
    
    if fetch_result is not None:
        if fetch_result[0] is not None:
            if ';' in fetch_result[0]:
                priceList = fetch_result[0].split(';')
    
    if len(priceList) == 2:
        if p_price < float(priceList[0]):
            mapping_price = 33
        elif p_price > float(priceList[0]) and p_price < float(priceList[1]):
            mapping_price = 66
        elif p_price > float(priceList[1]):
            mapping_price = 99
    
    if len(priceList) == 4:
        if p_price < float(priceList[0]):
            mapping_price = 20
        elif p_price > float(priceList[0]) and p_price < float(priceList[1]):
            mapping_price = 40
        elif p_price > float(priceList[1]) and p_price < float(priceList[2]):
            mapping_price = 60
        elif p_price > float(priceList[2]) and p_price < float(priceList[3]):
            mapping_price = 80
        elif p_price > float(priceList[3]):
            mapping_price = 100
    return mapping_price, len(priceList)

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

def select_match_from_pool(idices, poolList, final_matchList):
    for eleList in poolList:
        if len(eleList) > 0:
            if len(final_matchList) == 10:
                return final_matchList
            if len(eleList) > idices:
                if eleList[idices] > 0:# only choose these products that score greater than 0
                    selectedProduct_string = str(eleList[idices])
                    final_matchList.append(selectedProduct_string)
    return final_matchList

def update_info_to_website(productID, productInfo):
    db2 = pymysql.connect("158.132.123.119","root","tozmartdev2016","b2c-zw", 13306, charset="utf8")
    cursor2 = db2.cursor()

    sql_string = 'insert into `b2c-src`.product_maxmarch (idproduct, productlist) values (%s, %s)'
    product_data = (productID, productInfo)
    cursor2.execute(sql_string, product_data)
    db2.commit()#需要这一句才能保存到数据库中
    db2.close()
    


#this is the main function
if __name__ == '__main__':
    # this is the main function.
    db = pymysql.connect(host="localhost",
                         user="root",
                         password="123456",
                         db="clean_data_zalora",
                         charset="utf8")
    cursor = db.cursor()
    zaloraProducts = open("C:/Users/Administrator/Desktop/zalora4.txt", encoding='utf8').readlines()

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
        category_matchList_scoreList = [] # the score of the match category with the target product
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
            print('There category of this product is null. target_productID: ', target_productID)
            continue  #跳出此次for循环
        
        category_matchList, category_matchList_scoreList = find_category_level_match(target_product_category)
        if len(category_matchList) == 0:
            print('There is no match category of the product:', target_productID)
            continue
        
        # calculate the poollist of each category
        #1) if the featureList is null
        #2) if the featureList is not null
        feature_matchList, feature_scoreList = find_feature_level_match(target_product_category)
        
        if len(feature_matchList) == 0:# the featureList of the target product is null, the score is 0
            for ele_category_matchList in category_matchList: #find products pool in each match category.
                ele_match_productList = []
                ele_match_productList = find_products_with_no_featureLevel(ele_category_matchList)
                category_match_product_poolList.append(ele_match_productList)
            print('There is no feature match list, ProductID:', target_productID)

        if len(feature_matchList) > 0:# there are feature level matching
            feature_matchList_parent = find_feature_parent(feature_matchList) # the parent of feature level.
            diff_feature_matchList_parent = list(set(category_matchList) - set(feature_matchList_parent))# category_matchList - featurelist's parent.
            
            #calculate pool with features.
            if len(feature_matchList_parent) > 0:
                for ele_category_matchList in feature_matchList_parent: #find products pool in each match category.
                    ele_match_productList = []
                    #find the children of the category.
                    feature_children = find_children_feature_by_category_code(ele_category_matchList)
                    feature_under_the_category = list(set(feature_children)&set(feature_matchList))
                    ele_match_productList = find_products_with_featureLevel(ele_category_matchList, feature_under_the_category)
                    category_match_product_poolList.append(ele_match_productList)

            #calculate pool without features, category level
            if len(diff_feature_matchList_parent) > 0:
                for ele_category_matchList in diff_feature_matchList_parent: #find products pool in each match category.
                    ele_match_productList = []
                    ele_match_productList = find_products_with_no_featureLevel(ele_category_matchList)
                    category_match_product_poolList.append(ele_match_productList)
                    
        category_match_score_poolList = calculate_product_match_score(target_productInfoList, category_match_product_poolList, feature_matchList, feature_scoreList)
        category_match_score_poolList = MF.del_null_in_list(category_match_score_poolList)
        
        idicis = 0
        while len(final_matchList) < recNumber and idicis < recNumber:
            final_matchList = select_match_from_pool(idicis, category_match_score_poolList, final_matchList)
            idicis = idicis + 1
        with open('C:/Users/Administrator/Desktop/output4.txt','a', encoding='utf8') as f:
            f.write(str(target_productID) + '\t' + ';'.join(final_matchList) + '\n')
        
#         update_info_to_website(str(target_productID), ';'.join(final_matchList))
#         with open('C:/Users/Administrator/Desktop/output.txt','a', encoding='utf8') as f:
#             f.write(str(target_productID) + '\t' + target_product_category + '\t' + str(target_product_featureList) + '\t' + str(category_matchList) + '\t' + str(feature_matchList) + '\t' + str(final_matchList) + '\n')
    db.close()