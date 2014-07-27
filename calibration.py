import bgsa 
import os
import PIL
import csv 
import time
import glob
import pylab as pl

print "Debut de la calibration"


imgb = PIL.Image.open("calibration/gland_89_9.jpg")
imgr = PIL.Image.open("calibration/gland_89_0.jpg")



gold = csv.reader(open("gold_standard.csv","r"), delimiter=";")




goldData = dict()
for line in gold : 
	goldData[line[0]] = line[1]






c = csv.writer(open("calibration.csv", "w"))

def calibrate(value=-150):
	print "============== START ============================"
	for fichier in glob.glob("./calibration/*.jpg"):
		image   = PIL.Image.open(fichier)
		red     = bgsa.get_red(image,value)
		surface = c.writerow([fichier, red.histogram()[-1]])
		machine = float(red.histogram()[-1])

		key = fichier.replace(".jpg","").replace("./calibration/","")
		print key

		human 	= float(goldData[key])

		print fichier
		print "machine {}".format(machine) 
		print "human {}".format(human)
		machines.append(machine)
		humans.append(human)
		texts.append(key)

		

		print "======="

for i in range(150,300,10):
	machines = []
	humans   = []
	texts    = []
	calibrate(-i)
	pl.clf()
	pl.scatter(humans,machines)

	# for i, txt in enumerate(texts):
	# 	pl.annotate(txt, (humans[i],machines[i]))

	pl.savefig('calibrate-{}.png'.format(i))
	# pl.show()
