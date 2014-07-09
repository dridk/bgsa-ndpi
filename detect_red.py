from openslide import *
from argparse import ArgumentParser
import ImageEnhance
import time

# Settings arguments parser 
parser = ArgumentParser(description="compute a ndpi file")
parser.add_argument("filename")
args = parser.parse_args()



def get_red(source, brightness=0.06, contrast = 500):
	""" Return Red composante""" 
	image = source.convert("YCbCr")
	red   = image.split()[2];
	redBrighness = ImageEnhance.Brightness(red)
	red          = redBrighness.enhance(0.06)
	redContrast  = ImageEnhance.Contrast(red)
	red          = redContrast.enhance(500)
	return red


# Create OpenSlide object

ndpi        = OpenSlide(args.filename)
ndpi_width  = ndpi.dimensions[0]
ndpi_height = ndpi.dimensions[1]

print "LOAD {}".format(args.filename)
print "width:".ljust(20) + str(ndpi_width)
print "height:".ljust(20) + str(ndpi_height)
print "level count:".ljust(20) + str(ndpi.level_count)


# image = ndpi.get_thumbnail((500,500))
splitFactor = 2
level       = 7


total_width  = ndpi.level_dimensions[level][0]
total_height = ndpi.level_dimensions[level][1]

print "split image {}x{} , level:{} , factor:{}".format(total_width,total_height,level,splitFactor)
for i in range(splitFactor):
	for j in range(splitFactor):
		x     = i * ndpi_width / splitFactor
		y     = j * ndpi_height / splitFactor
		w     = total_width / splitFactor
		h     = total_height / splitFactor

		print "x:{:5} y:{:5} w:{:5}px h:{:5}px:".format(x,y,w,h)
		
		image = ndpi.read_region((x,y), level, (w, h))
		image.show()
		time.sleep(2)
		del(image)

print("end")

# get_red(image).show()
