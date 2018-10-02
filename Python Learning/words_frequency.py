# -*- coding: utf-8 -*-
import pymysql,re

def select_text_info(productID):
    output = ''
    sqlstring = 'select product_desc from testdb.product where idproduct = %s'
    cursor.execute(sqlstring, productID)
    
    fetch_result = cursor.fetchone()
    if fetch_result is not None:
        output = fetch_result[0]
    else:
        output = ''
    
    final_result = re.findall('[a-z-]{3,}', output.lower())
    return final_result

db = pymysql.connect("localhost","root","123456","testdb", charset="utf8")
cursor = db.cursor()

cateList = open("C:/Users/Administrator/Desktop/cates.txt", encoding='utf8').readlines()
productList = open("C:/Users/Administrator/Desktop/idandcates.txt", encoding='utf8').readlines()

productId_list = []
productcate_list = []


for each_product in productList:
    each_product = each_product.strip('\n')
    p_ele_list = each_product.split('\t')
    p_id = p_ele_list[0]
    productId_list.append(p_id)
    p_cate = p_ele_list[1]
    productcate_list.append(p_cate)


for each_category in cateList:
    each_p_words_all = []
    each_category = each_category.strip('\n')
    
    all_products_in_category = [i for i,a in enumerate(productcate_list) if a==each_category]
    
    for each_p in all_products_in_category:
        each_id = productId_list[each_p]
        each_product_word_list = select_text_info(each_id)
        each_p_words_all.extend(each_product_word_list)

    each_p_words_single = {}.fromkeys(each_p_words_all).keys()
    
    for ele in each_p_words_single:
        with open('C:/Users/Administrator/Desktop/wrods_frequency.txt','a', encoding='utf8') as f:
            f.write(each_category + '\t' + ele + '\t' + str(each_p_words_all.count(ele)) + '\n')
   
    




