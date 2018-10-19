# import the necessary packages
#######
####gfhfg

import cv2
import pytesseract

# load the image, convert it to grayscale, and blur it
image = cv2.imread("/home/kris/Рабочий стол/145.jpg")
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(gray, (3, 3), 0)
# detect edges in the image
edged = cv2.Canny(gray, 10, 250)


print(pytesseract.image_to_string(image))



cv2.imshow("Output", image)

cv2.imshow("Edged", edged)

cv2.waitKey(0)
