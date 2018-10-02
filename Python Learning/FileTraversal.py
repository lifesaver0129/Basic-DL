# -*- coding: utf-8 -*-


import os
import os.path
import re

folderList = ['C:/Users/Administrator/Desktop/Recategorization20170402/women1/']
for eachfolder in folderList:
#     subrootdir = rootdir + eachfolder + '/'
    subrootdir = eachfolder
    
    for parent, dirnames, filenames in os.walk(subrootdir):    #三个参数：分别返回1.父目录 2.所有文件夹名字（不含路径） 3.所有文件名字
    #     for dirname in  dirnames:                       #输出文件夹信息
    #         print("parent is: " + parent)
    #         print("dirname is: " + dirname)
        filenameList = []
        for filename in filenames:                        #输出文件信息
    #         print("parent is: " + parent)
    #         print("filename is: " + filename)
    #         print("the full name of the file is: " + os.path.join(parent, filename)) #输出文件路径信息
            if '_'in filename:
                productId = int(re.findall(r'[0-9]{6}', filename)[0])
                if productId not in filenameList:
                    filenameList.append(int(productId))
        for ele in filenameList:
            with open('C:/Users/Administrator/Desktop/categorylist.txt','a', encoding='utf8') as f:
                f.write(str(ele) + '\t' + parent.strip('/').split('/')[-1] + '\n')


