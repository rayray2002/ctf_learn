import cv2      #https://pypi.org/project/opencv-python/
import random
import string


flag = cv2.imread('flag_enc.png', cv2.IMREAD_GRAYSCALE)
golem = cv2.imread('golem_enc.png', cv2.IMREAD_GRAYSCALE)

h, w = flag.shape
for i in range(h):
    for j in range(w):
        flag[i][j] ^= golem[i][j]

cv2.imwrite('out.png', flag)