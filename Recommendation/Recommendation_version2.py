#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2017年1月13日
Recommendation Version 2
@author: Administrator
'''
import pymysql
import MyFunctions_productRecategorize as MF 
import nltk, re, random
import numpy as np
from difflib import SequenceMatcher

#************Start of function definition
def extract_Nouns(essays):
    nouns = []
    if essays is None:
        return nouns
    else:
        tokens = nltk.word_tokenize(essays)
        tagged = nltk.pos_tag(tokens)
        nouns = [word for word,pos in tagged \
            if (pos == 'NN' or pos == 'NNP' or pos == 'NNS' or pos == 'NNPS')]
    return nouns
    
#similarity of difflib
# def similar(a, b):
#     return SequenceMatcher(None, a, b).ratio()

def similar(list_a, list_b):
    return len(set(list_a)&set(list_b))

#Find product category list by product id
def find_product_category_by_ID(product_id):
    outputResult = []
    sql_find_product_category_by_id = "SELECT product_category FROM product where idproduct = %s"
    cursor.execute(sql_find_product_category_by_id, product_id)
    fetch_product_category_by_id_results = cursor.fetchone()
    
    if fetch_product_category_by_id_results[0] is not None:
        outputResult = fetch_product_category_by_id_results[0].split(';')
    return outputResult

#Find breadcrumbs by product id
def find_breadcrumbs_by_ID(product_id):
    outputResult = ''
    sql_fetch_product_breadcrumbs_by_id = "SELECT product_breadcrumbs FROM product where idproduct = %s"
    cursor.execute(sql_fetch_product_breadcrumbs_by_id, product_id)
    fetch_product_breadcrumbs_by_id_results = cursor.fetchone()
    if fetch_product_breadcrumbs_by_id_results is not None:
        if fetch_product_breadcrumbs_by_id_results[0] is not None:
            outputResult = fetch_product_breadcrumbs_by_id_results[0]
    return outputResult

#Find product colour by product id
def find_product_color_by_ID(product_id):
    outputResult = ''
    sql_fetch_product_colour_by_id = "SELECT product_details FROM product where idproduct = %s"
    cursor.execute(sql_fetch_product_colour_by_id, product_id)
    fetch_product_colour_by_id_results = cursor.fetchone()
    if fetch_product_colour_by_id_results[0] is not None:
        clour_list = fetch_product_colour_by_id_results[0].split('||')
        #print(clour_list)
        for ele in clour_list:
            if 'Colour' in ele:
                outputResult = ele[7:]
    return outputResult

#Find product list by breadcrumbs
def find_product_list_by_breadcrumbs(product_breadcrumbs):
    outputResult= []
    sql_fetch_productList_by_id = "SELECT idproduct FROM test.product where product_breadcrumbs = %s"
    cursor.execute(sql_fetch_productList_by_id, product_breadcrumbs)
    fetch_productList_by_id_results = cursor.fetchall()
    if fetch_productList_by_id_results is not None:
        for ele in fetch_productList_by_id_results:
            outputResult.append(ele[0])
    return outputResult

#get product description Method 1: find all of the description.
def find_product_desc_list_1(productID):
    outputString = ''
    sql_fetch_product_desc_by_id = "SELECT product_desc FROM product where idproduct = %s"
    cursor.execute(sql_fetch_product_desc_by_id, productID)
    fetch_product_desc_by_id_results = cursor.fetchone()
    
    if fetch_product_desc_by_id_results[0] is not None:
        outputString = fetch_product_desc_by_id_results[0]
    outputString = outputString.replace('\n', ' ')
    return outputString

#get product description Method 2: find only the keywords.
def find_product_desc_list_2(productID):
    rx = re.compile('\W+')
    productDescList = ""
    sql_fetch_product_desc_by_id = "SELECT product_desc FROM product where idproduct = %s"
    cursor.execute(sql_fetch_product_desc_by_id, productID)
    fetch_product_desc_by_id_results = cursor.fetchone()
    if fetch_product_desc_by_id_results[0] is not None:
        des_list = str(fetch_product_desc_by_id_results[0]).split('\n')
        #recategory list should be 2 normally, but exist length recategory =1
        if len(des_list) > 1:
            for ele in des_list:
                if ele[0:1] == '-':
                    productDescList = productDescList + ' ' + ele
            return rx.sub(' ', productDescList).strip()
        else:
            return str(fetch_product_desc_by_id_results[0]).strip()
    return ''

#get product description Method 3: find all the words cleaned words.
def find_product_desc_list_3(productID):
    rx = re.compile('\W+')
    sql_fetch_product_desc_by_id = "SELECT product_desc FROM product where idproduct = %s"
    cursor.execute(sql_fetch_product_desc_by_id, productID)
    fetch_product_desc_by_id_results = cursor.fetchone()
    if fetch_product_desc_by_id_results[0] is not None:
        return rx.sub(' ', fetch_product_desc_by_id_results[0]).strip()
    return ''
#****************************************

# find the colour type by colour name
def query_colour_type_num_by_colour(product_colour):
    outputInt = 0
    if product_colour != '':
        sql_query_colour_type_num_by_colour = "SELECT type_number FROM test.colour where description = %s"
        cursor.execute(sql_query_colour_type_num_by_colour, product_colour)
        query_colour_type_num_by_colour_result = cursor.fetchone()
        
        if query_colour_type_num_by_colour_result is not None:
            outputInt = query_colour_type_num_by_colour_result[0]
    return outputInt

# calculate the similarity of two colours
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
        
def query_colour_by_id(product_id):
#Find product colour by product id
    outputString = ''
    sql_query_colour_by_id = "SELECT product_details FROM product where idproduct = %s"
    cursor.execute(sql_query_colour_by_id, product_id)
    query_colour_by_id_results = cursor.fetchone()
    
    if query_colour_by_id_results is not None:
        if query_colour_by_id_results[0] is not None:
            clour_list = query_colour_by_id_results[0].split('||')
#             print(clour_list)
            for ele in clour_list:
                if 'Colour' in ele:
                    outputString = ele[7:].replace("\n", "").strip()
    return outputString.strip().lower()

def colour_similarity_by_id(product_id_1, product_id_2):
#     product_colour_1 = query_colour_by_id(product_id_1).lower()
#     product_colour_2 = query_colour_by_id(product_id_2).lower()
    product_colour_1 = query_colour_by_id(product_id_1)
    product_colour_2 = query_colour_by_id(product_id_2)

#     product_colour_1 = "".join((lambda x:(x.sort(),x)[1])(list(product_colour_1)))
#     product_colour_2 = "".join((lambda x:(x.sort(),x)[1])(list(product_colour_2)))

    if product_colour_1 == ''  or product_colour_2 == '':
        return 0
    else:
        return colour_similarity(product_colour_1, product_colour_2)
    
    
def recommendation(product_id):
    final_rec_list = []
    # find the breadcrumbs of the current product id
    breadcrumbs = zalora_content[zalora_id.index(product_id)].split('\t')[1]
    # find the list of product of the current product id with the same breadcrumbs
    product_list_in_breadcrumbs = find_product_list_by_breadcrumbs(breadcrumbs)
    content_product_id = zalora_content[zalora_id.index(product_id)].split('\t')[6].split(';') + \
                         zalora_content[zalora_id.index(product_id)].split('\t')[7].split(';')

    total_sim_list = []
    if len(product_list_in_breadcrumbs) > 200:
        product_list_in_breadcrumbs = random.sample(product_list_in_breadcrumbs, 200)
    
    for ele in product_list_in_breadcrumbs:
        # calculate the similarity of each product with the current product
        colour_simi = colour_similarity_by_id(product_id, ele)

        content_ele = zalora_content[zalora_id.index(ele)].split('\t')[6].split(';') + \
                          zalora_content[zalora_id.index(ele)].split('\t')[7].split(';')
                          
        txt_simi = similar(content_product_id, content_ele)*0.1

        total_simi = colour_simi * 0.5 + txt_simi
        total_sim_list.append(total_simi)

    # 按照相似度进行排序，并返回下标
    list_sorted_index = np.argsort(total_sim_list)

    # 截取相似度最大的20个下标
    if len(product_list_in_breadcrumbs) > 20:
        indices_list = list_sorted_index[-20:]
    else:
        indices_list = list_sorted_index

    # 根据下标和product_list_in_breadcrumbs找到product_id
    for indices_list_ele in indices_list:
        final_rec_list.append(product_list_in_breadcrumbs[indices_list_ele])

    # 删除自己的product_id
    if int(product_id) in final_rec_list:
        final_rec_list.remove(int(product_id))
    # 将list reverse
    final_rec_list.reverse()
    #将list转化为string
    string_final_rec_list = MF.list_to_string(final_rec_list)
    with open('C:/Users/Administrator/Desktop/recommendation_list.txt','a') as f:
        f.write(str(product_id) + '\t' + string_final_rec_list + '\n')

#************End of function definition
db = pymysql.connect("localhost","root","123456","test", charset="utf8")
cursor = db.cursor()

zalora_id = []
for ele in open("C:/Users/Administrator/Desktop/zalora_id.txt", encoding='utf8').readlines():
    ele = ele.strip('\n').strip('\ufeff')
    zalora_id.append(int(ele))

zalora_content = []
for ele in open("C:/Users/Administrator/Desktop/zalora with nouns and details.txt", encoding='utf8').readlines():
    ele = ele.strip('\n').strip('\ufeff')
    zalora_content.append(ele)

start = 30000
while start < 50000:
#     ele = ele.strip('\n')
    ele = zalora_id[start]
    print(start, ele)
    recommendation(ele)
    start = start + 1
db.close()
