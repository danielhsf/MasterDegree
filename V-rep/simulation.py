#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 10 09:46:31 2018

@author: robotica
"""
import vrep
import cv2
import numpy as np
import math
import matplotlib.pyplot as plt
import random

print ('Program started')
vrep.simxFinish(-1)
clientID=vrep.simxStart('127.0.0.1',19999,True,True,5000,5) 


if clientID!=-1:
    print ('Connected to remote API server')
    returnCode, depthCam = vrep.simxGetObjectHandle(clientID,'kinect_depth',vrep.simx_opmode_blocking)
    returnCode, colorCam = vrep.simxGetObjectHandle(clientID,'kinect_rgb',vrep.simx_opmode_blocking)
    res,resolution,image=vrep.simxGetVisionSensorImage(clientID,colorCam,1,vrep.simx_opmode_streaming)
    while (len(image) == 0):
        res,resolution,image=vrep.simxGetVisionSensorImage(clientID,colorCam,1,vrep.simx_opmode_buffer)
        
    returnCode, resolution, buffer =vrep.simxGetVisionSensorDepthBuffer(clientID,depthCam,vrep.simx_opmode_streaming)
    returnCode, eulerAngles = vrep.simxGetObjectOrientation(clientID, depthCam,-1, vrep.simx_opmode_streaming)
    while(len(buffer) == 0):
        returnCode, eulerAngles = vrep.simxGetObjectOrientation(clientID, depthCam,-1, vrep.simx_opmode_buffer)
        returnCode, resolution, buffer =vrep.simxGetVisionSensorDepthBuffer(clientID,depthCam,vrep.simx_opmode_buffer)
    
    
#Ajeitando a imagem
image = np.asarray(image)
image = np.flip(image,0)
#image = image + 128
image = np.reshape(image,(512,512))
image = image.astype(np.uint8)
cv2.imwrite("gray.png",image)

#Ajeitando a profundidade
buffer = np.asarray(buffer)
buffer = np.flip(buffer,0)
buffer = np.reshape(buffer,(512,512))


vrep.simxFinish(clientID)

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

img = cv2.imread("gray.png") 

depth = buffer

depth = 0.36+ depth*4 

h,w = depth.shape[:2]

cx = h/2
cy = w/2

constant = 570
pc = np.zeros((h,w,3),dtype= np.float32)

for v in range(0,h):
    for u in range(0,w):
        if(depth[v,u] != 0):
            z = depth[v,u]
            x = (v - cx)*z/constant
            y = (u - cy)*z/constant
            pc[v,u,0] = x
            pc[v,u,1] = y
            pc[v,u,2] = z


pca = np.zeros((h,w,3),dtype= np.float32)
theta = -math.pi/4
for v in range(0,h):
    for u in range(0,w):
        x = - (pc[v,u,0]*math.cos(theta) + pc[v,u,2]*math.sin(theta))
        y = pc[v,u,1]
        z = 0.8  + pc[v,u,0]*math.sin(theta) - pc[v,u,2]*math.cos(theta) 
        pca[v,u,0] = x
        pca[v,u,1] = y
        pca[v,u,2] = z

newimg = np.zeros((h*w,3),dtype = np.uint8)
cont = 0
for i in range(0,h):
    for j in range(0,w):
        newimg[cont] = img[i,j]
        cont+=1
        
x = pca[:,:,0]
y = pca[:,:,1]
z = pca[:,:,2]




#Usando o Método de RANSAC
pca = pca.reshape(-1, 3)
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

limiar = 0.01
best = 0
for i in range(0,100):
    t = random.sample(range(len(pca)), 3)
    plano = plane(pca[t[0]],pca[t[1]],pca[t[2]])
    match = fit(pca,plano,limiar)
    difzero = plano[0]*plano[0] + plano[1]*plano[1] + plano[2]*plano[2]
    if((match > best) & (difzero != 0)):
        best = match
        p = plano
        l = t
        

a,b,c,d = p
cont=0 
outrocont= 0
for j in pca:
    value = abs(j[0]*p[0] +  j[1]*p[1] + j[2]*p[2] + p[3])
    #value = abs(j[2] - (a*j[0]+b*j[1]+c))
    if (abs(value) < limiar):
        newimg[cont] = np.array([0,0,255], dtype=np.uint8)
        outrocont+=1
    cont+=1  
    

write_ply('Perspectiva.ply', pc, newimg)
write_ply('transformado.ply', pca, newimg)





























