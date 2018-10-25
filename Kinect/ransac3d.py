#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 17 11:49:08 2018

@author: robotica
"""
import cv2
import matplotlib.pyplot as plt
import numpy as np

ply_header = '''ply
format ascii 1.0
element vertex %(vert_num)d
property float x
property float y
property float z
property uchar red
property uchar green
property uchar blue
end_header
'''

def write_ply(fn, verts, colors):
    verts = verts.reshape(-1, 3)
    colors = colors.reshape(-1, 3)
    verts = np.hstack([verts, colors])
    with open(fn, 'wb') as f:
        f.write((ply_header % dict(vert_num=len(verts))).encode('utf-8'))
        np.savetxt(f, verts, fmt='%f %f %f %d %d %d ')


img = cv2.imread("img.png")
data = cv2.FileStorage("pt.yaml",cv2.FileStorage_READ)
dados = data.getNode("PointCloud").mat()
#dados = dados/8
#dados = dados.astype(np.uint8)
#dados = cv2.resize(dados,(160,120))
#dados = dados.astype(np.float64)
distance = np.zeros((480,640),dtype=np.float64)
#depthInMeters = 1.0 / (rawDepth * -0.0030711016 + 3.3309495161);
for i in range(0,480):
    for j in range(0,640):
        if(dados[i,j] < 2047):
            distance[i,j] = (1.0 / ((dados[i,j]*-0.0030711016) + 3.3309495161));
            if(distance[i,j]>4):
                distance[i,j] = 4
        else:
            distance[i,j] = 4

img = cv2.resize(img,(640,480))
xyz = np.zeros((640*480,3),dtype = np.float64)
uvq = np.zeros((640*480,3),dtype = np.float64)
mtx = np.array([[621.40562026, 0, 310.51277384], [0, 639.96310931, 357.51762425], [0,0,1]])
fx = 621.40562026
Cx = 310.51277384
fy = 639.96310931
Cy = 357.51762425
cont = 0
for i in range(480):
    for j in range(640):
        u = (i-Cx)/fx
        v = (j-Cy)/fy
        if(dados[i,j] == 0):
            xyz[cont] = np.array([i,j,dados[i,j]])
            uvq[cont] = np.array([u,v,0.8])
        elif(dados[i,j] == 255):
            xyz[cont] = np.array([i,j,dados[i,j]])
            uvq[cont] = np.array([u,v,4])
        else:
            xyz[cont] = np.array([i,j,dados[i,j]])
            uvq[cont] = np.array([u,v,distance[i,j]])
        cont+=1

newimg = np.zeros((640*480,3),dtype = np.uint8)
cont = 0
for i in range(480):
    for j in range(640):
        newimg[cont] = img[i,j]
        cont+=1
cv2.imwrite("depth.png",dados)

write_ply('novo.ply', uvq, newimg)