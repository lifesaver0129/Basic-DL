'''
Created on 2016年8月19日

@author: Administrator
'''
import re,os,urllib.request
from macpath import split

def saveImgs(img_path, img_url, img_name):
    if not os.path.exists(img_path):  ###判断文件是否存在，返回布尔值
        os.makedirs(img_path)
    save_path = img_path + '/' + img_name + '.jpg'
    urllib.request.urlretrieve(img_url, save_path)


file = open("C:/Users/Administrator/Desktop/photo.txt")
while 1:
    line = file.readline()
    if not line:
        break
    sepline = str(line).split(',')
    print(sepline[0], sepline[1].strip('\n'))
    try:
        saveImgs('C:/Users/Administrator/Desktop/photo', sepline[1].strip('\n'), sepline[0])
    except:
        print("This url is available")

file.close()