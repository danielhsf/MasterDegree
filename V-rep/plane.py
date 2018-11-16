
import numpy, random, math
import sys
from datetime import datetime

#arg1: nome do arquivo pcd
#arg2: limiar que define a distancia vertical maxima para pertencer ao plano, depende da nuvem
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

def write_ply(fn, verts):
    with open(fn, 'wb') as f:
        f.write((ply_header % dict(vert_num=len(verts))).encode('utf-8'))
        numpy.savetxt(f, verts, fmt='%f %f %f %d %d %d ')


f = open("transformado.ply", 'r')
print("transformado.ply")
random.seed(datetime.now())

for i in range(0,10):
    a = f.readline()

p = []
newp = []
for line in f:
	n1, n2, n3, n4, n5, n6 = (float(s) for s in line.split())
	p.append((n1, n2, -n3)),newp.append((n1,n2,-n3, n4, n5, n6))
f.close()

best = 0, 0, 0, 0

n = 10
limiar = float(0.1)
for i in range(100):
	t = random.sample(range(len(p)), n)
	pts = []
	for j in t:
		pts.append(p[j])

	sum_x = 0
	sum_xx = 0
	sum_y = 0
	sum_yy = 0
	sum_xy = 0
	sum_xz = 0
	sum_yz = 0
	sum_z = 0

	for k in t:
		x, y, z = p[k]
		sum_x += x
		sum_y += y
		sum_z += z
		sum_yy += y*y
		sum_xx += x*x
		sum_xy += x*y
		sum_xz += x*z
		sum_yz += y*z

	a, b, c = numpy.linalg.solve([[sum_x, sum_y, n],[sum_xy, sum_yy, sum_y],[sum_xx, sum_xy, sum_x]],[sum_z, sum_yz, sum_xz])

	total = 0
	desvio = 0
	for j in p:
		delta = abs(j[2] - (a*j[0]+b*j[1]+c))
		desvio += (j[2] - (a*j[0]+b*j[1]+c))**2
		if delta < limiar:
			total += 1

	if total > best[3]:
		best = a, b, c, total
	print(i, a, b, c, total, best[3])

print(best)
print('gnuplot: splot \"nuvem2.xyz\", \"nuvem1.xyz\", ' + str(best[0]) + '*x+' + str(best[1]) + '*y+' + str(best[2]))

#grava em arquivos diferentes os dois subconjuntos de pontos (proximo ao plano e afastados do plano)
#n1 = open('nuvem1.ply', 'w+')
#n2 = open('nuvem2.ply', 'w+')
#a, b, c = best[0:3]
#for j in newp:
#    delta = abs(j[2] - (a*j[0]+b*j[1]+c))
#    if delta < limiar:
#        n1.write(str(j[0]) + ' ' + str(j[1]) + ' ' + str(j[2]) + ' ' + str(int(j[3])) + ' ' + str(int(j[4])) + ' ' + str(int(j[5])) +'\n')
#    else:
#        n2.write(str(j[0]) + ' ' + str(j[1]) + ' ' + str(j[2]) + ' ' + str(int(j[3])) + ' ' + str(int(j[4])) + ' ' + str(int(j[5])) +'\n')
#
#n1.close()
#n2.close()

plano = numpy.zeros((0,6))
restante = numpy.zeros((0,6))
a, b, c = best[0:3]
for j in newp:
    delta = abs(j[2] - (a*j[0]+b*j[1]+c))
    if (delta < limiar):
        plano = numpy.append(plano,[j],axis=0)
    else:
        restante = numpy.append(plano,[j],axis=0)

write_ply('plano.ply', plano)
write_ply('restante.ply', restante)

print(len(plano) + len(restante))