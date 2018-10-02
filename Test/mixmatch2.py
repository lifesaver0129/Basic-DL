#!/usr/bin/env python
# -*- coding: utf-8 -*-

import MyFunctions as MF
import pymysql, nltk
import re, random
import numpy as np
from numpy import average


def find_product_info(productID):
    outputList = []
    sqlString = "SELECT * FROM clean_data_zalora.product where idproduct = %s"

    cursor.execute(sqlString, productID)
    fetch_result = cursor.fetchone()

    if fetch_result is not None:
        for ele_fetch_result in fetch_result:
            outputList.append(ele_fetch_result)
    return outputList


def find_match_category(category_codeList):
    outputString = []
    sqlString = "select path from test.category where code = %s"
    if len(category_codeList) > 0:
        for ele in category_codeList:
            cursor.execute(sqlString, ele)
            fetch_result = cursor.fetchone()

            if fetch_result is not None:
                for ele in fetch_result:
                    outputString.append(ele)
    return outputString


def find_category_level_match(product_category):
    matchList = []
    scorelist = []

    sqlString = 'SELECT matchcategorycode, score FROM clean_data_zalora.mix_match_pairs where categorycode = %s and level = %s'
    cursor.execute(sqlString, (product_category, '1'))  # first level category match
    fetch_result = cursor.fetchall()

    if fetch_result is not None:
        for ele_fetch_result in fetch_result:
            matchList.append(ele_fetch_result[0])
            scorelist.append(ele_fetch_result[1])
    return matchList, scorelist


def find_feature_level_match(product_featureList):
    matchcategoryList = []
    scorelist = []

    if len(product_featureList) > 0:
        for ele in product_featureList:
            sqlString = 'SELECT matchcategorycode, score from mix_match_pairs where categorycode = %s and matchcategorycode like %s'
            cursor.execute(sqlString, (ele, '%F%'))
            fetch_result = cursor.fetchall()

            if fetch_result is not None:
                for ele_fetch_result in fetch_result:
                    matchcategoryList.append(ele_fetch_result[0])
                    scorelist.append(float(ele_fetch_result[1]))
    return matchcategoryList, scorelist


def find_products_by_categoryLevel(categorylevelcode):
    outputList = []

    sqlString = 'SELECT idproduct from product where category = %s'
    cursor.execute(sqlString, categorylevelcode)
    fetch_result = cursor.fetchall()

    if fetch_result is not None:
        for ele_fetch_result in fetch_result:
            outputList.append(ele_fetch_result[0])
    return outputList


def assign_category_lvl_product_number(categoryList):
    outputList = []
    numberlist = []

    nbase = 12 / len(categoryList)
    for ele in categoryList:
        if ele not in outputList:
            cnumber = 0
            cnumber = categoryList.count(ele)
            productNumber = round(cnumber * nbase)
            if productNumber < 1:
                productNumber = 1
            numberlist.append(productNumber)
            outputList.append(ele)
    return outputList, numberlist


def find_product_info_by_productID(productID):
    outputList = []
    sqlString = 'Select product_brand, product_price, feature_list from test.product where idproduct = %s'

    cursor.execute(sqlString, productID)
    fetch_result = cursor.fetchall()

    if fetch_result is not None:
        for ele_fetch_result in fetch_result:
            outputList.append(ele_fetch_result[0])
            outputList.append(re.findall(r'[1-9]+\.*[0-9]*', ele_fetch_result[1])[0])
            outputList.append(ele_fetch_result[2])
    return outputList


def calculate_match_score(target_productID, product_2, feature_matchList, feature_scoreList):
    final_score = 0

    brand_score = 0
    price_score = 0
    feature_match_score = 0

    product_info_1 = find_product_info_by_productID(target_productID)
    product_info_2 = find_product_info_by_productID(product_2)

    if product_info_1[0] == product_info_2[0]:
        brand_score = 1

    if float(product_info_1[1]) != 0 and float(product_info_2[1]) != 0:
        if abs(float(product_info_1[1]) - float(product_info_2[1])) / float(product_info_1[1]) < 0.2:
            price_score = 1

    product_2_featureList = product_info_2[2].split(';')
    if len(MF.list_intersection(feature_matchList, product_2_featureList)) > 0:
        for iNumber in range(len(feature_matchList)):
            if feature_matchList[iNumber] in product_2_featureList:
                feature_match_score = feature_match_score + feature_scoreList[iNumber]
        feature_match_score = feature_match_score / len(MF.list_intersection(feature_matchList, product_2_featureList))

    final_score = (brand_score + price_score) / 2 + feature_match_score * 2
    return final_score


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


def process_feature_and_category_matchList(category_level_matchList, feature_level_matchList):
    category_without_branch = []

    category_with_branch = find_parent_category(feature_level_matchList)
    category_without_branch = list(set(category_level_matchList) ^ set(category_with_branch))

    return category_with_branch, category_without_branch


def find_match_pool(category_no_branch):
    outputList = []
    sqlString = 'SELECT idproduct FROM test.product where category_1_lvl = %s'
    cursor.execute(sqlString, category_no_branch)
    fetch_result = cursor.fetchall()

    if fetch_result is not None:
        for ele_fetch_result in fetch_result:
            outputList.append(ele_fetch_result[0])
    return outputList


def find_category_match_productList(productID, category_match_pool, assignedNumber):
    assignedNumber = round(assignedNumber)
    outputList = []
    scoreList = []
    for i in range(len(category_match_pool)):
        score = calculate_match_score(productID, category_match_pool[i], [], [])
        scoreList.append([i, score])
    # find the most highest score product. sort the 2nd number
    scoreList.sort(key=lambda x: x[1])

    for ele in scoreList[-1 * assignedNumber:]:
        outputList.append(category_match_pool[ele[0]])
    return outputList


def find_feature_match_productList(productID, category_match_pool, assignedNumber, feature_matchList,
                                   feature_scoreList):
    assignedNumber = round(assignedNumber)
    outputList = []
    scoreList = []
    for i in range(len(category_match_pool)):
        score = calculate_match_score(productID, category_match_pool[i], feature_matchList, feature_scoreList)
        scoreList.append([i, score])
    # find the most highest score product. sort the 2nd number
    scoreList.sort(key=lambda x: x[1])

    for ele in scoreList[-1 * assignedNumber:]:
        outputList.append(category_match_pool[ele[0]])
    return outputList


def find_product_match_score(productInfoList, category_match_product_poolList, feature_matchList, feature_scoreList):
    product_matchList = []
    for i in range(len(category_match_product_poolList)):
        ele_category_scoreList = []
        ele_category_scoreList = calculate_match_score_in_category(productInfoList, category_match_product_poolList[i],
                                                                   feature_matchList, feature_scoreList)
        product_matchList.append(ele_category_scoreList)
    return product_matchList


def calculate_match_score_in_category(productInfoList, product_list, feature_matchList, feature_scoreList):
    match_score_in_category = []
    templist = []
    for ele in product_list:
        matchScore = calculate_match_score_for_each_product(productInfoList, ele, feature_matchList, feature_scoreList)
        templist.append(matchScore)
    # sorting the indices of the templist in reverse way.
    indiceList = [i[0] for i in sorted(enumerate(templist), key=lambda x: x[1])][::-1]

    for ele in indiceList:
        temp = product_list[ele]
        match_score_in_category.append(temp)
    return match_score_in_category


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


def calculate_match_score_for_each_product(productInfoList, ele, feature_matchList, feature_scoreList):
    final_score = 0

    brand_score = 0
    price_score = 0
    color_score = 0
    feature_match_score = 0

    match_product_info = find_product_info(ele)
    # sequence is idproduct, breadcrumbs, title, brand, gender, price, description, colour, category, feature

    if productInfoList[3] == match_product_info[3]:
        brand_score = 1

    if colour_similarity(productInfoList[7], match_product_info[7]) == 1:
        brand_score = 1

    if float(productInfoList[5]) != 0 and float(match_product_info[5]) != 0:
        if abs(float(productInfoList[5]) - float(match_product_info[5])) / float(productInfoList[5]) < 0.2:
            price_score = 1

    match_product_featureList = match_product_info[9].split(';')
    if len(MF.list_intersection(feature_matchList, match_product_featureList)) > 0:
        scorelist = []
        for iNumber in range(len(feature_matchList)):
            if feature_matchList[iNumber] in match_product_featureList:
                scorelist.append(feature_scoreList[iNumber])
        feature_match_score = sum(scorelist) / len(MF.list_intersection(feature_matchList, match_product_featureList))

    final_score = brand_score * 0.4 + price_score * 0.3 + color_score * 0.3 + feature_match_score
    return final_score


def select_match_from_pool(idices, poolList, outputList):
    for eleList in poolList:
        if len(outputList) == 10:
            return outputList
        outputList.append(eleList[idices])
    return outputList


if __name__ == '__main__':
    # this is the main function.
    db = pymysql.connect(host="localhost",
                         user="root",
                         password="123456",
                         db="clean_data_zalora",
                         charset="utf8")
    cursor = db.cursor()
    zaloraProducts = open("C:/Users/Administrator/Desktop/new_zalora_id.txt", encoding='utf8').readlines()

    for productID in zaloraProducts:  # Define, Call this productID as target product.
        recNumber = 10
        # define the parameters.
        productID = productID.strip('\n')  # the product ID of the target product.
        productID = 342

        print(productID)
        # find product_category, product_featureList and gender from category_mapping Table.
        productInfoList = find_product_info(productID)
        product_category = productInfoList[8]
        product_featureList = productInfoList[9].split(';')  # given a product, features selected under the category.
        product_gender = productInfoList[4]

        final_matchList = []  # the final result
        # productID = 1645

        category_matchList = []  # the match list of the product category.
        category_scoreList = []  # the score of the match category with the target product
        category_numberList = []  # the number of products assigned to each match category.

        category_match_product_poolList = []  # list on list
        category_match_pool = []  # the candidate products in category level.

        feature_matchList = []  # the match list of the product feature.
        feature_scoreList = []  # the score of the match feature with the target product

        category_no_branch = []  # subbranch of category, there is no feature matches in the category.
        category_with_branch = []  # subbranch of category, there are feature matches in the category.

        ele_category_match_productList = []  # the match products in category level.
        ele_feature_match_productList = []  # the match products in feature level.

        # find category level match
        if len(product_category) == 0:  # there is no match in category level, no match in the last.
            print('There is no matching product. ProductID: ', productID)
            continue  # 跳出此次for循环

        category_matchList, category_scoreList = find_category_level_match(product_category)

        if len(category_matchList) == 0:  # there is no match in category level, no match in the last.
            print('There is no matching product. ProductID: ', productID)
            continue  # 跳出此次for循环

        if len(category_matchList) > 0:
            # print(categor_and_number)
            for ele_category_matchList in category_matchList:  # find products pool in each match category.
                ele_match_productList = []
                ele_match_productList = find_products_by_categoryLevel(ele_category_matchList)
                category_match_product_poolList.append(ele_match_productList)
            # find feature level match
            if len(product_featureList) > 0:
                feature_matchList, feature_scoreList = find_feature_level_match(product_featureList)

            category_match_score_poolList = find_product_match_score(productInfoList, category_match_product_poolList,
                                                                     feature_matchList, feature_scoreList)
            category_match_score_poolList = MF.del_null_in_list(category_match_score_poolList)
            idicis = 0
            while len(final_matchList) < 10:
                final_matchList = select_match_from_pool(idicis, category_match_score_poolList, final_matchList)
                idicis = idicis + 1
            print(final_matchList)

            #         with open('C:/Users/Administrator/Desktop/output.txt','a', encoding='utf8') as f:
            #             f.write(str(productID) + '\t' + product_category + '\t' + str(product_featureList) + '\t' + str(category_matchList) + '\t' + str(feature_matchList) + '\t' + str(final_matchList) + '\n')

    db.close()