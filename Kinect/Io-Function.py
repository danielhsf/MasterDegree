#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 22 16:16:16 2018

@author: robotica
"""
import cv2
import numpy as np

def Io(O,m,n):
    if((m<0) or (n<0)):
        return 0
    else:
        return O[m,n] + Io(O,m-1,n) + Io(O,m,n-1) - Io(O,m-1,n-1)

def S(io,m,n,r):
    return 1/(4*r**2)*(io[m+r,n+r]-io[m-r,n+r]-io[m+r,n-r]+io[m-r,n-r])

data = cv2.FileStorage("pt.yaml",cv2.FileStorage_READ)
dados = data.getNode("PointCloud").mat()
dados = dados/8
dados = dados.astype(np.uint8)

cv2.imwrite("depth.png",dados)

integral = cv2.integral(dados)
integral = integral[1:481,1:641]

print(S(integral,240,320,10))
print(S(integral,240,320,150))

import matplotlib.pyplot as plt 

plt.imshow(dados)




