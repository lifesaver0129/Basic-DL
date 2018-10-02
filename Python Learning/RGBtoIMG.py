# -*- coding: utf-8 -*-
'''
Created on 2017年1月3日

@author: Administrator
'''
from PIL import Image

pantoneRGBs = open("C:/Users/Administrator/Desktop/PANTONE U.txt", encoding='utf8').readlines()

pantoneList = []

for ele_pantoneRGBs in pantoneRGBs:
    ele_pantoneRGBs = ele_pantoneRGBs.strip('\n')
    ele_pantoneRGBsList = ele_pantoneRGBs.split('\t')
    IMGname = ele_pantoneRGBsList[0]
    
    rgblist = []
    for ele in ele_pantoneRGBsList[1].split(','):
        rgblist.append(int(ele))
    
    im = Image.new("RGB",(200,200), tuple(rgblist))#创建图片
    im.save('C:/Users/Administrator/Desktop/PANTONE U/' + IMGname + '.jpg')