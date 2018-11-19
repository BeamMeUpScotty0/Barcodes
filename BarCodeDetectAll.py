from PIL import Image
import os
import cv2
import glob


import os
import numpy as np
import cv2
from os import listdir,makedirs
from os.path import isfile,join

c = 0

print("Resizing...")

directory = '/home/kris/Рабочий стол/Dataset/еще датасет/New Folder//'
new_directory = '/home/kris/Рабочий стол/Dataset/еще датасет/small/'


path = r'/home/kris/Рабочий стол/Dataset/еще датасет/train_with22/' # Source Folder
dstpath = r'/home/kris/Рабочий стол/Dataset/еще датасет/Codes_farmed/' # Destination Folder
dstpath2 = r'/home/kris/Рабочий стол/Dataset/еще датасет/Codes_BW/' # Destination Folder



for file_name in os.listdir(directory):
  print("Resizing %s" % file_name)
  image = Image.open(os.path.join(directory, file_name))
  new_dimensions = (360, 480)
  output = image.resize(new_dimensions, Image.ANTIALIAS)

  output_file_name = os.path.join(new_directory, "small_" + file_name)

  output.save(output_file_name, "JPEG", quality = 95)
  c += 1

print("All done ", c)



print("Processing...")


try:
    makedirs(dstpath)
except:
    print ("Directory already exist, images will be written in the same folder")

# Folder won't used
files = [f for f in listdir(path) if isfile(join(path,f))]

for image in os.listdir(new_directory):
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


        dstPath = join(dstpath, image)
        cv2.imwrite(dstPath, img)

        dstPath2 = join(dstpath2, image)
        cv2.imwrite(dstPath2, closed)


    except:
        print ("{} is not converted".format(image))
