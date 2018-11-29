#!/usr/bin/env python
import freenect
import cv2
import frame_convert2
import numpy as np

cv2.namedWindow('Depth')
cv2.namedWindow('Video')
print('Press ESC in window to stop')


def get_depth():
    return frame_convert2.pretty_depth_cv(freenect.sync_get_depth()[0])

def get_depth2():
    return freenect.sync_get_depth()[0]

def get_video():
    return frame_convert2.video_cv(freenect.sync_get_video()[0])

#img = np.array(get_depth2())
#print(img)

#cv2.imshow('imagem',img)
#cv2.waitKey()
fs = cv2.FileStorage("pt.yaml",flags = cv2.FileStorage_WRITE + cv2.FileStorage_FORMAT_YAML)

fs.write("PointCloud",get_depth2())

cv2.imwrite("img.png",get_video())
cv2.imwrite("depth.png",get_depth2())

while 1:
    cv2.imshow('Depth', get_depth())
    cv2.imshow('Video', get_video())
    if cv2.waitKey(10) == 27:
        break


#import time
#time.sleep(60)
#for cont in range (0,120):
#	img = get_video()
#	#img = cv2.cvtColor(img, cv2.CV_RGB2GRAY)
#	cv2.imwrite("images/"+str(cont)+".png",img)
	


