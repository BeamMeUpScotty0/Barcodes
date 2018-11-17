
import numpy as np
import cv2
import glob

from os import listdir
from os.path import isfile, join
import numpy
import cv2



image0 = cv2.imread("/home/kris/Рабочий стол/resized/P81117-173535.jpg")
image = cv2.resize(images, (360, 460))
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


gradX = cv2.Sobel(gray, ddepth=cv2.CV_64F, dx=1, dy=0, ksize=-1)
gradY = cv2.Sobel(gray, ddepth=cv2.CV_64F, dx=0, dy=1, ksize=-1)

# subtract the y-gradient from the x-gradient
gradient = cv2.subtract(gradX, gradY)
gradient = cv2.convertScaleAbs(gradient)

blurred = cv2.blur(gradient, (9, 9))
(_, thresh) = cv2.threshold(blurred, 225, 255, cv2.THRESH_BINARY)
# construct a closing kernel and apply it to the thresholded image




#21- много мелких деталей, 49 - крупное фот
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (49, 7))
closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

closed = cv2.erode(closed, None, iterations = 4)
closed = cv2.dilate(closed, None, iterations = 4)

#(cnts, _) = cv2.findContours(closed.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
(_, cnts, _) = cv2.findContours(closed.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#_, contours = cv2.findContours(closed.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
c = sorted(cnts, key=cv2.contourArea, reverse=True)[0]

# compute the rotated bounding box of the largest contour
rect = cv2.minAreaRect(c)
box = np.int0(cv2.boxPoints(rect))

# draw a bounding box arounded the detected barcode and display the
# image
cv2.drawContours(image, [box], -1, (0, 255, 0), 3)
cv2.drawContours(closed, [box], -1, (255, 255, 255), 3)


cv2.imshow("Image0", closed)
cv2.imshow("Image", image)

cv2.imwrite('/home/kris/Рабочий стол/Desktop/cv/small/0pic.jpg', image)
cv2.imwrite('/home/kris/Рабочий стол/Desktop/cv/small/pic.jpg', closed)
cv2.waitKey(0)
