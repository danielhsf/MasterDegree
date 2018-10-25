#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  2 13:59:06 2018

@author: robotica
"""

import cv2
from GetSmooth import smooth
import numpy as np
import matplotlib.pyplot as plt

# Getting the Image 
img = cv2.imread("img.png",0)
img = cv2.resize(img,(160,120))
#img = img[200:240,280:320]
plt.imshow(img)
# Getting the Depths
fs = cv2.FileStorage("pt.yaml",cv2.FileStorage_READ)
depth = fs.getNode("PointCloud").mat()
#
newdepth = smooth(depth)
import random

for t in range (0,51):
    x = random.randint(0,480)
    y = random.randint(0,640)
    p1 = np.array([x, y, newdepth[x][y]])
    p2 = np.array([x, y, newdepth[x][y]])
    p3 = np.array([x, y, newdepth[x][y]])

    # These two vectors are in the plane
    v1 = p2 - p1
    v2 = p3 - p1
    
    # the cross product is a vector normal to the plane
    cp = np.cross(v1, v2)
    a, b, c = cp
    
    # This evaluates a * x3 + b * y3 + c * z3 which equals d
    d = np.dot(cp, p3)
    
    print('The equation is {0}x + {1}y + {2}z = {3}'.format(a, b, c, d))
    x = []
    y = []
    z = []
    epsilon = 50
    for i in range (0,480):
        for j in range(0,640):
            value = abs(a*i + b*j +c*depth[i][j] - d)/((a**2+b**2+c**2)**0.5)
            if(value<epsilon):
                img[i][j] = 5*t

plt.imshow(img)
