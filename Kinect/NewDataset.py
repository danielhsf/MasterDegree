#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 31 14:13:38 2018

@author: robotica
"""
import cv2
import numpy as np

img = cv2.imread("table_1_1.png")
depth = cv2.imread("table_1_1_depth.png",0)

print(np.max(depth))