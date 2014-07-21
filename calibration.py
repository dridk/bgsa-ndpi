from detect_red import * 
import os
import PIL
import csv 

print "Debut de la calibration"

c = csv.writer(open("calibration.csv", "w"))

for fichier in os.listdir("calibration"):
	image   = PIL.Image.open("calibration/"+fichier)
	red     = get_red(image)
	surface =	c.writerow([fichier, red.histogram()[-1]])
