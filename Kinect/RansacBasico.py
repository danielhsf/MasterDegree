#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov  3 01:11:03 2018

@author: daniel
"""
import numpy as np
import random
import cv2

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

def plane(p2,p1,p0):
    u = p2 - p0
    v = p1 - p0
    cp = np.cross(u,v)
    a,b,c = cp
    d = - np.dot(cp,p2)
    plano = np.array([a,b,c,d])
    return plano

def fit(pontos,plano,limiar):
    cont = 0
    for i in range(0,len(pontos)):
        value = plano[0]*pontos[i][0] + plano[1]*pontos[i][1] + plano[2]*pontos[i][2] + plano[3]
        if(abs(value) < limiar):
            cont+=1
    return cont

img = cv2.imread("00000-color.png",cv2.IMREAD_ANYCOLOR) 

depth = cv2.imread("00000-depth.png", cv2.IMREAD_ANYDEPTH)

h,w = depth.shape[:2]

depth = np.float32(depth)

cx = 240
cy = 320

constant = 570.3

MM_per_m = 1000

pc = np.zeros((0,0,3),dtype= np.float64)
for v in range(0,h):
    for u in range(0,w):
        if(depth[v,u] != 0):
            z = depth[v,u]/MM_per_m
            x = (v - cx)*z/constant
            y = (u - cy)*z/constant
            #pc[v,u,0] = x
            #pc[v,u,1] = y
            #pc[v,u,2] = z
            pc = np.append(pc,[[x,y,z]])
            #pc.append(np.array([x,y,z]))

pc = pc.reshape(-1, 3)

limiar = 0.6


best = 0
p = []
l = []
plano = np.zeros((0,6))
nplano = np.zeros((0,3))
rgb = np.array([[0,0,255],[255,0,0]])

for x in range(0,2):
    for i in range(0,100):
        t = random.sample(range(len(pc)), 3)
        plano = plane(pc[t[0]],pc[t[1]],pc[t[2]])
        match = fit(pc,plano,limiar)
        difzero = plano[0]*plano[0] + plano[1]*plano[1] + plano[2]*plano[2]
        if((match > best) & (difzero != 0)):
            best = match
            p = plano
            l = t
            
    
    a,b,c,d = p
    for j in pc:
        value = abs(j[0]*p[0] +  j[1]*p[1] + j[2]*p[2] + p[3])
        #value = abs(j[2] - (a*j[0]+b*j[1]+c))
        if value < limiar:
            plano = np.append(plano,[j[0],j[1],j[2],rgb[x][0],rgb[x][1],rgb[x][2]])
        else:
            nplano = np.append(nplano,[j[0],j[1],j[2]])
            
    plano = plano.reshape(-1,6)
    
    pc = nplano.reshape(-1,3)
    
    

#grava em arquivos diferentes os dois subconjuntos de pontos (proximo ao plano e afastados do plano)
n1 = open('nuvem1.ply', 'wb')
n2 = open('nuvem2.ply', 'wb')
n1.write((ply_header % dict(vert_num=len(plano))).encode('utf-8'))
n2.write((ply_header % dict(vert_num=len(nplano))).encode('utf-8'))

np.savetxt(n1, plano, fmt='%f %f %f %d %d %d ')
np.savetxt(n2, nplano, fmt='%f %f %f %d %d %d ')

n1.close()
n2.close()











































