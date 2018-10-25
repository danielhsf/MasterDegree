#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 21 18:14:48 2018

@author: robotica
"""

import cv2
import numpy as np

Maior = np.zeros((4,2),dtype= np.uint8)
xy = np.zeros((4,2),dtype= np.uint8)

Maior[0,0]=0
Maior[0,1]=0
Maior[1,0]=1
Maior[1,1]=0
Maior[2,0]=0
Maior[2,1]=1
Maior[3,0]=1
Maior[3,1]=1


xy[0,0]=1
xy[0,1]=2
xy[1,0]=4
xy[1,1]=6
xy[2,0]=6
xy[2,1]=8
xy[3,0]=9
xy[3,1]=12


r,i = cv2.estimateAffine2D(Maior,xy,inliers = 1,method = cv2.RANSAC)

Maior = np.zeros((4,3),dtype= np.uint8)
xy = np.zeros((4,3),dtype= np.uint8)

Maior[0,0]=0
Maior[0,1]=0
Maior[0,2]=0

Maior[1,0]=1
Maior[1,1]=0
Maior[1,2]=0

Maior[2,0]=0
Maior[2,1]=1
Maior[2,2] =0

Maior[3,0]=0
Maior[3,1]=0
Maior[3,2]=1

xy[0,0]=1
xy[0,1]=2
xy[0,2]=3

xy[1,0]=4
xy[1,1]=5
xy[1,2]=6

xy[2,0]=7
xy[2,1]=8
xy[2,2]=9

xy[3,0]=10
xy[3,1]=11
xy[3,2]=12

retval, out, inliers = cv2.estimateAffine3D(Maior,xy,None,inliers = 1)