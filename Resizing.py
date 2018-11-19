from PIL import Image
import os
import cv2
import glob

c = 0

directory = '/home/kris/Рабочий стол/Dataset/Train/No_Big/'
new_directory = '/home/kris/Рабочий стол/Dataset/Train/No_Small/'

for file_name in os.listdir(directory):
  print("Processing %s" % file_name)
  image = Image.open(os.path.join(directory, file_name))
  new_dimensions = (360, 480)
  output = image.resize(new_dimensions, Image.ANTIALIAS)

  output_file_name = os.path.join(new_directory, "small_" + file_name)

  output.save(output_file_name, "JPEG", quality = 95)
  c += 1

print("All done ", c)
