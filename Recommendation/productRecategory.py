'''
Created on 2016年10月25日

@author: Administrator
'''
import MyFunctions_productRecategorize as MF

categoryPath = "C:/Users/Administrator/Desktop/keywordmen.txt"
# categoryPath = "C:/Users/Administrator/Desktop/test/W input _tracy20161201.txt"

productContentPath = "C:/Users/Administrator/Desktop/cleanwomeninput.txt"

# featurePath = "C:/Users/Administrator/Desktop/M input F_tracy20161203.txt"
# featurePath = "C:/Users/Administrator/Desktop/W inputF _tracy20161203.txt"

# read product content
list_productID, list_title_1, list_bread_2, list_description_3 = \
MF.readProductContentIntoList(productContentPath)

category_list, keyword_list = MF.readKeywordsIntoList(categoryPath)

recategory_result_A = MF.recategorize(list_title_1, category_list, keyword_list)
recategory_result_B = MF.recategorize(list_bread_2, category_list, keyword_list)
recategory_result_C = MF.recategorize(list_description_3, category_list, keyword_list)

# hitA_C = MF.hit_decision(recategory_result_A, recategory_result_C)
# hitB_C = MF.hit_decision(recategory_result_B, recategory_result_C)
# 
# finalResult = MF.final_decision(hitA_C, hitB_C)
finalResult = MF.recategorize2(recategory_result_A, recategory_result_B, recategory_result_C) 

finalResultNoDuplicate = []
for ele_finalResult in finalResult:
    ele_finalResultlist = MF.del_string_duplicates(ele_finalResult)
    finalResultNoDuplicate.append(ele_finalResultlist)

for i in range(len(list_productID)):
    print(list_productID[i])
#     print(list_productID[i])
    with open('C:/Users/Administrator/Desktop/recategory.txt','a', encoding='utf8') as f:
        f.write(str(list_productID[i]) + '\t' + list_title_1[i] + '\t' + list_bread_2[i] + '\t' + list_description_3[i] + '\t' + recategory_result_A[i] + '\t' + recategory_result_B[i] + '\t' + \
                recategory_result_C[i] + '\t' + finalResultNoDuplicate[i] + '\n')
