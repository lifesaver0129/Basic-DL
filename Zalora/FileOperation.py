'''
Created on 2016年8月5日

@author: Administrator
'''

import csv, os
import pymysql

def readURL(dir_path, file_name):
    #写入csv文件 文件名
    LIST = []
    f = open(dir_path + file_name)
    reader = csv.reader(f)
    try:
        for line in reader:
            LIST.append(line[0])
        return LIST
        f.close()
    except:
        print('line contains NULL byte')
        f.close()

def GetFileNameAndExt(filename):
    shot_name, ext_name = filename.split('.')
    return shot_name


def walk_dir(dir_path,fileinfo,topdown=True):
    for root, dirs, files in os.walk(dir_path, topdown):
        for name in files:
            category_name = GetFileNameAndExt(os.path.join(name))
            print(category_name)


dir_path = 'C:/Users/Administrator/Desktop/'

#category name of all categories.读取这个目录下的所有文件名
category_list = readURL(dir_path,"1.csv")
#incease_num = 1
final_list = []
list_number = []
for category_ele in category_list:
    list_number.append(category_ele.count('%'))


#this is the position list of value == 1
list_position_lv1 = [i for i,x in enumerate(list_number) if x==0]
list_position_lv2 = [i for i,x in enumerate(list_number) if x==1]
list_position_lv3 = [i for i,x in enumerate(list_number) if x==2]
list_position_lv4 = [i for i,x in enumerate(list_number) if x==3]
list_position_lv5 = [i for i,x in enumerate(list_number) if x==4]

list_position_lv1_content = []
for ele in list_position_lv1:
    ele_content = category_list[ele]
    final_list.append(ele_content)

list_position_lv2_content = []
for ele in list_position_lv2:
    ele_content = category_list[ele]
    final_list.append(ele_content)

list_position_lv3_content = []
for ele in list_position_lv3:
    ele_content = category_list[ele]
    split_ele = ele_content.split('%')
    final_list.append(ele_content)
    final_list.append(split_ele[0] + '%' +split_ele[1])
    
list_position_lv4_content = []
for ele in list_position_lv4:
    ele_content = category_list[ele]
    split_ele = ele_content.split('%')
    final_list.append(ele_content)
    final_list.append(split_ele[0] + '%' + split_ele[1] + '%' + split_ele[2])

list_position_lv4_content = []
for ele in list_position_lv5:
    ele_content = category_list[ele]
    split_ele = ele_content.split('%')
    final_list.append(ele_content)
    final_list.append(split_ele[0] + '%' + split_ele[1] + '%' + split_ele[2] + '%' + split_ele[3])


l2 = []    
for i in final_list:    
    if not i in l2:    
        l2.append(i)    


  
for ele in l2:
    print(ele)