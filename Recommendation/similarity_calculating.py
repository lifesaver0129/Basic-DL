# -*- coding: utf-8 -*-

import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

def find_n_similar(M, category_list):
    result_list = []
    for inumber in range(len(M)):
        eachrow = M[inumber]
        rowresult = []
        row_indices = eachrow.argsort()[-51:][::-1] #find 10 most similar
        rowresult = [category_list[i] for i in row_indices]
        result_list.append(rowresult)
        with open('C:/Users/Administrator/Desktop/womenwrongid.txt','a', encoding='utf8') as f:
            if category_list[inumber] in rowresult:
                rowresult.remove(category_list[inumber])
            f.write(category_list[inumber] + '\t' + ';'.join(rowresult) + '\n')
    return result_list
 
if __name__ == '__main__':
    cate_info_list = open("C:/Users/Administrator/Desktop/cate_info_list.txt", encoding='utf8').readlines()# categories
    all_info_list = open("C:/Users/Administrator/Desktop/all_info_list.txt", encoding='utf8').readlines()# all info list
 
#     ids = open("C:/Users/Administrator/Desktop/ids.txt", encoding='utf8').readlines()# categories
#     idandcate = open("C:/Users/Administrator/Desktop/idandcate.txt", encoding='utf8').readlines()# all info list
    list_productID = []
    list_cate = []
    for eachrow in all_info_list:
        eachrow = eachrow.strip('\n')
        eachrowList = eachrow.split('\t')
        ele_ID = str(int(eachrowList[0]))
        list_productID.append(ele_ID)
        ele_category = eachrowList[1]
        list_cate.append(ele_category)
   
    for each_category in cate_info_list:
        print(each_category.strip('\n'))
        each_category = each_category.strip('\n')
        ids_in_category = []
        indices = [i for i, x in enumerate(list_cate) if x == each_category]
        ids_in_category = [list_productID[i] for i in indices]
          
        if len(ids_in_category) > 2:
            xiangliang_list = []
            similarity_matrix = []
            for each_product in ids_in_category:
                each_xiangliang = []
                each_xiangliang = all_info_list[list_productID.index(each_product)].strip('\n').split('\t')[2:]
 
                each_xiangliang = [float(i) for i in each_xiangliang]
                xiangliang_list.append(each_xiangliang)
            similarity_matrix = cosine_similarity(np.array(xiangliang_list))
            find_n_similar(similarity_matrix, ids_in_category)
#     listid = []
#     for ele in idandcate:
#         ele = ele.strip('\n')
#         listid.append(ele.split('\t')[0])
#     for id in ids:
#         id = id.strip('\n')
#         with open('C:/Users/Administrator/Desktop/womenwrongid.txt','a', encoding='utf8') as f:
#             f.write(idandcate[listid.index(id)].strip('\n') + '\n')
