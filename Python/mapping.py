#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 24 20:02:01 2018

@author: robotica
"""
import numpy as np

def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return array[idx]

def place(line,floor,table,degree):
    x, y, z = line.split(" ")
    x = float(x)
    y = float(y)
    z = float(z)
    chao = np.array([7.56478e-05, 0.094037, 0.995569, -0.0753264])
    tab =  np.array([3.82002e-05, 0.0934332, 0.995626, -0.254958])
    deg =  np.array([1.69712e-06, -0.995455, -0.09523, 0.797903])
    epsilon = np.zeros(3)
    epsilon[0] = x*chao[0] + y*chao[1] + z*chao[2] + chao[3]
    epsilon[1] = x*deg[0] + y*deg[1] + z*deg[2] + deg[3]
    epsilon[2] = x*tab[0] + y*tab[1] + z*tab[2] + tab[3]
    a = find_nearest(epsilon, 0)
    a = np.where(epsilon == a)[0]
    if(a == 0):
        print("chao")
        floor+=1
    elif(a == 1):
        print("degrau")
        table+=1
    else:
        print("tabua Vertical")
        degree+=1
    return floor,table,degree
    
file = open("3-obstaculo.pcd","r")

for i in range(0,11):
    line = file.readline()

floor = 0
table = 0
degree = 0

points = np.zeros((0,3))

for line in file:
    floor, table, degree = place(line,floor,table,degree)
    vetor = line.replace("\n","")
    vetor = vetor.split(" ")
    vetor = np.array([float(vetor[0]), float(vetor[0]), float(vetor[0])])
    
