#-*- coding: UTF-8 -*-
'''
Created on Oct 18, 2016

@author: wei
'''
from skimage import io, data
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
from scipy import misc
#from ctypes.wintypes import RGB

if __name__ == '__main__':
    #打开image文件
    img_input = Image.open('2.jpg')
    img_input = np.array(img_input).astype('uint8')

    img = misc.imread('image_received2.png','RGB')
    #img = Image.open('image_received2.png')
    
    #plot画图 显示图片
    plt.imshow(img, vmin=0, vmax=18)
    plt.show()
    
    im = np.array(img).astype('uint8')
    #显示尺寸im.shape is the height and width of the img
    print(im.shape)    #plt.imshow(img)

    print(np.unique(im))
    dress_p = np.where(im == 7,1,0).astype('uint8')
    
    #生成图像大小的矩阵
    dress_p1 = np.zeros(img_input.shape)

    for i in range(3):
        dress_p1[:,:,i] = dress_p
    dress = dress_p1*img_input
    
    #plot画图 显示图片
    plt.imshow(dress)
    plt.show()
    