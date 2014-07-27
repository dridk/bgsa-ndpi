import bgsa 
import os
import PIL
import csv 
import time

print "Debut de la calibration"


imgb = PIL.Image.open("calibration/gland_89_9.jpg")
imgr = PIL.Image.open("calibration/gland_89_0.jpg")



gold = csv.reader(open("gold_standard.csv","r"), delimiter=";")




goldData = dict()
for line in gold : 
	goldData[line[0]] = line[1]




listDiff = []

c = csv.writer(open("calibration.csv", "w"))

print "============== START ============================"
for fichier in os.listdir("calibration"):
	image   = PIL.Image.open("calibration/"+fichier)
	red     = bgsa.get_red(image)
	surface = c.writerow([fichier, red.histogram()[-1]])
	machine = float(red.histogram()[-1])

	print(goldData[fichier.replace(".jpg","")])

	human 	= float(goldData[fichier.replace(".jpg","")])

	print fichier
	print "machine {}".format(machine) 
	print "human {}".format(human)

	try: 
		diff = machine / human
	except:
		diff = 0

	if diff is not 0:
		listDiff.append(diff)

	print "diff {}".format(diff)

	print "======="


print "min: {0} - max: {1}".format(min(listDiff), max(listDiff))


