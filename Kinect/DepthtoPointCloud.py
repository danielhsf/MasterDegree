#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  1 16:12:05 2018

@author: robotica
"""
import cv2
import numpy as np

ply_header = '''ply
format ascii 1.0
element vertex %(vert_num)d
property float x
property float y
property float z
property uchar blue
property uchar green
property uchar red
end_header
'''

def write_ply(fn, verts, colors):
    verts = verts.reshape(-1, 3)
    colors = colors.reshape(-1, 3)
    verts = np.hstack([verts, colors])
    with open(fn, 'wb') as f:
        f.write((ply_header % dict(vert_num=len(verts))).encode('utf-8'))
        np.savetxt(f, verts, fmt='%f %f %f %d %d %d ')

img = cv2.imread("00000-color.png",cv2.IMREAD_ANYCOLOR) 

depth = cv2.imread("00000-depth.png", cv2.IMREAD_ANYDEPTH)

h,w = depth.shape[:2]

depth = np.float32(depth)

cx = 240
cy = 320

constant = 570.3

MM_per_m = 1000

pc = np.zeros((h,w,3),dtype= np.float32)

for v in range(0,h):
    for u in range(0,w):
        z = depth[v,u]/MM_per_m
        x = (v - cx)*z/constant
        y = (u - cy)*z/constant
        pc[v,u,0] = x
        pc[v,u,1] = y
        pc[v,u,2] = z
        
newimg = np.zeros((640*480,3),dtype = np.uint8)
cont = 0
for i in range(480):
    for j in range(640):
        newimg[cont] = img[i,j]
        cont+=1

write_ply('novo.ply', pc, newimg)