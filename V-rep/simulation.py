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
    while(len(buffer) == 0):
        returnCode, resolution, buffer =vrep.simxGetVisionSensorDepthBuffer(clientID,depthCam,vrep.simx_opmode_buffer)
    
    
#Ajeitando a imagem
image = np.asarray(image)
#image = np.flip(image,0)
#image = image + 128
image = np.reshape(image,(512,512))
image = image.astype(np.uint8)
cv2.imwrite("gray.png",image)

#Ajeitando a profundidade
buffer = np.asarray(buffer)
#buffer = np.flip(buffer,0)
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
        np.savetxt(f, verts, fmt='%f %f %f %d %d %d')

pcd_header = '''ply
format ascii 1.0
element vertex %(vert_num)d
property float x
property float y
property float z
property float rgb
end_header
'''
def write_pcd(fn, verts, colors):
    verts = verts.reshape(-1, 3)
    verts = np.hstack([verts, colors])
    with open(fn, 'wb') as f:
        f.write((ply_header % dict(vert_num=len(verts))).encode('utf-8'))
        np.savetxt(f, verts, fmt='%f %f %f %f')

img = cv2.imread("gray.png") 
depth = buffer
h,w = depth.shape[:2]
depth = 0.4+ depth*3.6 

newimg = np.zeros((h*w,3),dtype = np.uint8)
cont = 0
for i in range(0,512):
    for j in range(0,512):
        newimg[cont] = img[i,j]
        #newimg[cont] = test[0]<<16 | test[1]<<8 | test[2]
        cont+=1

pcdimg = np.zeros((h*w,1),dtype =np.uint32)
cont = 0
for i in range(0,512):
    for j in range(0,512):
        test = img[i,j]
        pcdimg[cont] = test[2]<<16 | test[1]<<8 | test[0]
        cont+=1

cx = h/2
cy = w/2

constant = 570
pc = np.zeros((h,w,3),dtype= np.float32)
for u in range(0,h):
    for v in range(0,w):
        z = depth[v,u]
        x = (u - cx)*z/constant
        y = (v - cy)*z/constant
        pc[v,u,0] = x
        pc[v,u,1] = y
        pc[v,u,2] = z


pca = np.zeros((h,w,3),dtype= np.float32)
theta = 180*math.pi/180
for v in range(0,h):
    for u in range(0,w):
        x = pc[v,u,0]
        y = pc[v,u,1]*math.cos(theta) - pc[v,u,2]*math.sin(theta)
        z = pc[v,u,1]*math.sin(theta) + pc[v,u,2]*math.cos(theta) + 0.8
        pca[v,u,0] = x
        pca[v,u,1] = y
        pca[v,u,2] = z

         
xc = pc[:,:,0]
yc = pc[:,:,1]
zc = pc[:,:,2]

xa = pca[:,:,0]
ya = pca[:,:,1]
za = pca[:,:,2]

write_ply('Perspectiva.ply', pc, newimg)
write_pcd('pcd.ply', pc, pcdimg)

##Usando o Método de RANSAC
#pca = pca.reshape(-1, 3)
#best = 0, 0, 0, 0
#n = 10
#limiar = float(0.1)
#for i in range(100):
#	t = random.sample(range(len(pca)), n)
#	pts = []
#	for j in t:
#		pts.append(pca[j])
#
#	sum_x = 0
#	sum_xx = 0
#	sum_y = 0
#	sum_yy = 0
#	sum_xy = 0
#	sum_xz = 0
#	sum_yz = 0
#	sum_z = 0
#
#	for k in t:
#		x, y, z = pca[k]
#		sum_x += x
#		sum_y += y
#		sum_z += z
#		sum_yy += y*y
#		sum_xx += x*x
#		sum_xy += x*y
#		sum_xz += x*z
#		sum_yz += y*z
#
#	a, b, c = np.linalg.solve([[sum_x, sum_y, n],[sum_xy, sum_yy, sum_y],[sum_xx, sum_xy, sum_x]],[sum_z, sum_yz, sum_xz])
#
#	total = 0
#	desvio = 0
#	for j in pca:
#		delta = abs(j[2] - (a*j[0]+b*j[1]+c))
#		desvio += (j[2] - (a*j[0]+b*j[1]+c))**2
#		if delta < limiar:
#			total += 1
#
#	if total > best[3]:
#		best = a, b, c, total
#	print(i, a, b, c, total, best[3])
#
#plano = np.zeros((0,3))
#restante = np.zeros((0,3))
#a, b, c = best[0:3]
#for j in pca:
#    delta = abs(j[2] - (a*j[0]+b*j[1]+c))
#    if (delta < limiar):
#        plano = np.append(plano,[[j[0],j[1],j[2]]],axis=0)
#    else:
#        restante = np.append(restante,[[j[0],j[1],j[2]]],axis=0)
#
#imgplano = np.zeros((len(plano), 3), dtype=np.uint8)
#write_ply('plano.ply', plano,imgplano)
#imgrestante = np.zeros((len(restante),3), dtype=np.uint8)
#write_ply('restante.ply', restante,imgrestante)
#
#print(len(plano) + len(restante))

#Desenhando o grid
#grid = np.zeros((300,300),dtype= np.uint8)*255
#
#xa = xa*100
#xa = xa.reshape(-1)
#xa = xa.astype(np.uint16)
#
#ya = ya + np.max(ya)
#ya = ya*100
#ya = ya.astype(np.uint16)
#ya = ya.reshape(-1)
#
#
#za = za - np.min(za)
#za = np.round(za,1)
#za[za == 0] = 255
#za[za!=255] = 0
#
##za= za.astype(np.uint8)
#za = za.reshape(-1)
#pd = np.zeros((128*128,3),dtype= np.uint16) 
#
#
#
#pd[:,0] = xa
#pd[:,1] = ya
#pd[:,2] = za
#
#for i in range (0,len(pd)):
#    grid[pd[i,0],pd[i,1]] = int(pd[i,2])
#    
#cv2.imwrite("grid.png",grid)


























