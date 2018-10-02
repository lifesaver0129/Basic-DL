#-*- coding: UTF-8 -*-
'''
Created on Oct 23, 2016

@author: wei
'''
import matplotlib.pyplot as plt
import numpy as np

from skimage import io, data



img = data.chelsea()
plt.imshow(img, vmin=0, vmax=18)
im = np.array(img).astype('uint8')
print im.shape    #plt.imshow(img)

plt.show()
