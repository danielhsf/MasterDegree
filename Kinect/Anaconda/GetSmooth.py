#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  2 14:11:44 2018

@author: robotica
"""
import numpy as np

def smooth(d):
    w,h = d.shape
    newdepth = np.zeros((w,h),np.uint16)
    for i in range(1,w-1):
        for j in range(1,h-1):
            newdepth[i][j] = int((d[i-1][j-1]+d[i-1][j]+d[i-1][j+1]+d[i][j-1]+d[i][j]+d[i][j+1]+d[i+1][j-1]+d[i+1][j]+d[i+1][j+1])/9)
    return newdepth