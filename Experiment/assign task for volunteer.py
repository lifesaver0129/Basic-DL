# -*- coding: utf-8 -*-
'''
Created on 2017年1月12日

@author: Administrator
'''

import random

number_of_list = 150#number of products in groups
number_of_volunteers = 50#number of volunteers
repeat_times = 5#repeat times of each product
number_of_products = 15# number of products selected for each volunteer


# random choose 5 products for each user.
#generate 50 no repeat numbers.


products = open("C:/Users/Administrator/Desktop/products.txt", encoding='utf8').readlines()

product_id_list = []
for ele in products:
    ele = ele.strip('\n')
    product_id_list.append(ele)

all_list = []
for i in range(repeat_times):
    temp = random.sample(range(0, number_of_list), number_of_list)
    all_list = all_list + temp

# print(all_list)

start_number = 0
end_numbser = number_of_products
for j in range(number_of_volunteers):
    volunteer_list = []
    while start_number < end_numbser:
        volunteer_list.append(product_id_list[all_list[start_number]])
        start_number = start_number + 1

    start_number = end_numbser
    end_numbser = start_number + number_of_products
    print(str(j) + '\t' + str(volunteer_list))


