import math

yaw = 0
roll =  -135*math.pi/180
pitch = 0

cy = math.cos(yaw * 0.5)
sy = math.sin(yaw * 0.5);
cr = math.cos(roll * 0.5)
sr = math.sin(roll * 0.5)
cp = math.cos(pitch * 0.5)
sp = math.sin(pitch * 0.5)

qw = cy * cr * cp + sy * sr * sp;
qx = cy * sr * cp - sy * cr * sp;
qy = cy * cr * sp + sy * sr * cp;
qz = sy * cr * cp - cy * sr * sp;

print(qw)
print(qx)
print(qy)
print(qz)
