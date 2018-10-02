# -*- coding: utf-8 -*-

'''
Created on 2016年8月30日
@author: Administrator
'''
import nltk, re, pymysql

from difflib import SequenceMatcher

def extractNouns(essays):
    if essays is None:
        return ''
    else:
        tokens = nltk.word_tokenize(essays)
        tagged = nltk.pos_tag(tokens)
        nouns = [word for word,pos in tagged \
            if (pos == 'NN' or pos == 'NNP' or pos == 'NNS' or pos == 'NNPS')]
        return nouns
    
#similarity of difflib
def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


#Find product category list by product id
def findProductCategoryByID(product_id):
    sql_fetch_product_category_by_id = "SELECT product_category FROM product where idproduct = %s"
    cursor.execute(sql_fetch_product_category_by_id, product_id)
    fetch_product_category_by_id_results = cursor.fetchone()
    if fetch_product_category_by_id_results[0] is not None:
        return fetch_product_category_by_id_results[0].split(';')
    else:
        return ""

#Find product title by product id
def findProductTitleByID(product_id):
    sql_fetch_product_title_by_id = "SELECT product_title FROM product where idproduct = %s"
    cursor.execute(sql_fetch_product_title_by_id, product_id)
    fetch_product_title_by_id_results = cursor.fetchone()
    if fetch_product_title_by_id_results[0] is not None:
        return fetch_product_title_by_id_results[0]
    else:
        return ""

#Find breadcrumbs by product id
def findProductBreadcrumbsByID(product_id):
    sql_fetch_product_breadcrumbs_by_id = "SELECT product_breadcrumbs FROM product where idproduct = %s"
    cursor.execute(sql_fetch_product_breadcrumbs_by_id, product_id)
    fetch_product_breadcrumbs_by_id_results = cursor.fetchone()
    if fetch_product_breadcrumbs_by_id_results[0] is not None:
        return fetch_product_breadcrumbs_by_id_results[0]
    else:
        return ""

#Find product colour by product id
def findProductColorByID(product_id):
    sql_fetch_product_colour_by_id = "SELECT product_details FROM product where idproduct = %s"
    cursor.execute(sql_fetch_product_colour_by_id, product_id)
    fetch_product_colour_by_id_results = cursor.fetchone()
    if fetch_product_colour_by_id_results[0] is not None:
        clour_list = fetch_product_colour_by_id_results[0].split('||')
        #print(clour_list)
        for ele in clour_list:
            if 'Colour' in ele:
                return ele[7:]
    return ''


#Find product material by product id
def findProductMaterialByID(product_id):
    sql_fetch_product_details_by_id = "SELECT product_details FROM product where idproduct = %s"
    cursor.execute(sql_fetch_product_details_by_id, product_id)
    fetch_product_details_by_id_results = cursor.fetchone()
    if fetch_product_details_by_id_results[0] is not None:
        material = fetch_product_details_by_id_results[0].split('||')
        #print(material)
        for ele in material:
            if 'Composition' in ele:
                return ele[12:].replace('\n','')
    return ''

#Find product list by breadcrumbs
def findProductListByBreadcrumbs(product_breadcrumbs):
    product_list = []
    sql_fetch_productList_by_id = "SELECT idproduct FROM product where product_breadcrumbs = %s"
    cursor.execute(sql_fetch_productList_by_id, product_breadcrumbs)
    fetch_productList_by_id_results = cursor.fetchall()
    if fetch_productList_by_id_results[0] is not None:
        for ele in fetch_productList_by_id_results:
            product_list.append(ele[0])
    return product_list

#get product description Method 1: find all of the description.
def getProductDescList_1(productID):
    sql_fetch_product_desc_by_id = "SELECT product_desc FROM product where idproduct = %s"
    cursor.execute(sql_fetch_product_desc_by_id, productID)
    fetch_product_desc_by_id_results = cursor.fetchone()
    if fetch_product_desc_by_id_results[0] is not None:
        return fetch_product_desc_by_id_results[0]

#get product description Method 2: find only the keywords.
def getProductDescList_2(productID):
    rx = re.compile('\W+')
    productDescList = ""
    sql_fetch_product_desc_by_id = "SELECT product_desc FROM product where idproduct = %s"
    cursor.execute(sql_fetch_product_desc_by_id, productID)
    fetch_product_desc_by_id_results = cursor.fetchone()
    if fetch_product_desc_by_id_results[0] is not None:
        des_list = str(fetch_product_desc_by_id_results[0]).split('\n')
        #test list should be 2 normally, but exist length test =1
        if len(des_list) > 1:
            for ele in des_list:
                if ele[0:1] == '-':
                    productDescList = productDescList + ' ' + ele
            return rx.sub(' ', productDescList).strip()
        else:
            return str(fetch_product_desc_by_id_results[0]).strip()
    return ''

#get product description Method 3: find all the words cleaned words.
def getProductDescList_3(productID):
    rx = re.compile('\W+')
    sql_fetch_product_desc_by_id = "SELECT product_desc FROM product where idproduct = %s"
    cursor.execute(sql_fetch_product_desc_by_id, productID)
    fetch_product_desc_by_id_results = cursor.fetchone()
    if fetch_product_desc_by_id_results[0] is not None:
        return rx.sub(' ', fetch_product_desc_by_id_results[0]).strip()
    return ''

# 打开数据库连接
db = pymysql.connect("localhost","root","123456","testdb", charset='utf8')
# 使用cursor()方法获取操作游标 
cursor = db.cursor()
#print(str(getProductDescList_1(21)))

numzero = 70001
#print(extractNouns(str(getProductDescList_1(2))))

# product_breadcrumbs = findProductBreadcrumbsByID(2)
# print(product_breadcrumbs)
# 
# colour = codecs.open("colour.txt", "w", "utf-8")
# material = codecs.open("material.txt", "w", "utf-8")
# #print(findProductMaterialByID(6770))
while numzero == 70001:
    #colour.write(str(numzero) + '\t' + findProductColorByID(numzero) + '\n')
    #material.write(str(numzero) + '\t' + findProductMaterialByID(numzero) + '\n')
    #print(findProductColorByID(50164))
    if len(findProductTitleByID(numzero))>1:
        for ele in findProductListByBreadcrumbs(findProductBreadcrumbsByID(numzero)):
            print(ele, '\t', similar(str(getProductDescList_3(numzero)), str(getProductDescList_3(ele))), '\t', findProductColorByID(ele))
        print('-----------')
    numzero = numzero + 1
# colour.close()
# material.close()

# for listele in findProductListByBreadcrumbs(product_breadcrumbs):
#     print(listele,'\t',similar(str(getProductDescList(40128)), str(getProductDescList(listele))))

# for listele in findProductListByBreadcrumbs(product_breadcrumbs):
#     numberzero = 0
#     if getProductDescList_1(listele) is not None:
#         for ele in extractNouns(getProductDescList_3(2)):
#             if ele in extractNouns(getProductDescList_3(listele)):
#                 numberzero = numberzero + 1
#     print(listele, '\t', numberzero)
    
    
    #print(extractNouns(getProductDescList_1(numzero)))
    #print(numzero, str(getProductDescList2(numzero)))
#     if similar(str(getProductDescList(6488)), str(getProductDescList(numzero))) > 0.5:
#         print(similar(str(getProductDescList(6488)), str(getProductDescList(numzero))))
#    print(similar(extractNouns(str(getProductDescList_1(2))), extractNouns(str(getProductDescList_1(numzero)))))
#     if ngram.NGram.compare(str(getProductDescList(46000)), str(getProductDescList(numzero)),N=2)>0.85:
#         print(numzero,ngram.NGram.compare(str(getProductDescList(46000)), str(getProductDescList(numzero)),N=2))
#     if similar(str(getProductDescList2(40276)), str(getProductDescList2(numzero))) > 0.4:
#         print(numzero,similar(str(getProductDescList2(40276)), str(getProductDescList2(numzero))))
#    numzero = numzero + 1
db.close()


