import os
import numpy as np
import cv2
from os import listdir,makedirs
from os.path import isfile,join

path = r'/home/kris/Рабочий стол/no_res' # Source Folder
dstpath = r'/home/kris/Рабочий стол/no_bw' # Destination Folder
dstpath2 = r'/home/kris/Рабочий стол/no_framed' # Destination Folder
c=0
try:
    makedirs(dstpath)
except:
    print ("Directory already exist, images will be written in asme folder")

# Folder won't used
files = [f for f in listdir(path) if isfile(join(path,f))]

for image in files:
    try:
        img = cv2.imread(os.path.join(path,image))
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        gradX = cv2.Sobel(gray, ddepth=cv2.CV_64F, dx=1, dy=0, ksize=-1)
        gradY = cv2.Sobel(gray, ddepth=cv2.CV_64F, dx=0, dy=1, ksize=-1)
        gradient = cv2.subtract(gradX, gradY)
        gradient = cv2.convertScaleAbs(gradient)


        blurred = cv2.blur(gradient, (9, 9))
        (_, thresh) = cv2.threshold(blurred, 225, 255, cv2.THRESH_BINARY)

        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (49, 7))
        closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

        closed = cv2.erode(closed, None, iterations=4)
        closed = cv2.dilate(closed, None, iterations=4)

        # (cnts, _) = cv2.findContours(closed.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        (_, cnts, _) = cv2.findContours(closed.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        # _, contours = cv2.findContours(closed.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        c = sorted(cnts, key=cv2.contourArea, reverse=True)[0]

        # compute the rotated bounding box of the largest contour
        rect = cv2.minAreaRect(c)
        box = np.int0(cv2.boxPoints(rect))

        cv2.drawContours(img, [box], -1, (0, 255, 0), 3)
        cv2.drawContours(closed, [box], -1, (255, 255, 255), 3)


       # dstPath = join(dstpath, image)
        dstPath2 = join(dstpath2, closed)
       # cv2.imwrite(dstPath,img)
        cv2.imwrite(dstPath2, closed)


    except:
        print ("{} is not converted".format(image))

