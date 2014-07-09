from openslide import *
from argparse import ArgumentParser
import ImageEnhance
import ImageOps
import ImageStat
import time
import numpy as np
from scipy.ndimage import morphology
from progress.bar import Bar



# ========== FUNCTION ===================================

def get_red(source, brightness=0.06, contrast = 500):
	""" Return Red composante""" 
	image = source.convert("YCbCr")
	red   = image.split()[2];
	redBrighness = ImageEnhance.Brightness(red)
	red          = redBrighness.enhance(0.06)
	redContrast  = ImageEnhance.Contrast(red)
	red          = redContrast.enhance(500)
	return red

def get_surface(source):
	"""Return Image Surface """

	brightness  = ImageEnhance.Brightness(source)
	img         = brightness.enhance(1.2)
	contrast    = ImageEnhance.Contrast(img)
	img         = contrast.enhance(2000)
	img         = ImageOps.grayscale(img)
	img         = ImageOps.invert(img)
	# # 	#Use NDImage to detect holes 
	ndarray     = np.array(img)
	ndarray     = morphology.binary_fill_holes(ndarray).astype(bool)
	ndarray     = morphology.binary_opening(ndarray,iterations=1)
	img          = Image.fromarray(np.uint8(ndarray*255))
	img          = img.convert("1")
	return img



# ========== Main ===================================

# Settings arguments parser 
parser = ArgumentParser(description="compute a ndpi file")
parser.add_argument("filename")
parser.add_argument("-s", "--split", default=2,  type=int)
parser.add_argument("-l", "--level", default=4,  type=int)
parser.add_argument("-d", "--debug", default=False,  type=bool)

args = parser.parse_args()

splitFactor = args.split
level       = args.level
debug       = args.debug


# Create OpenSlide object

ndpi        = OpenSlide(args.filename)
ndpi_width  = ndpi.dimensions[0]
ndpi_height = ndpi.dimensions[1]

print "================ START ================="
print "LOAD {}".format(args.filename)
print "width:".ljust(20) + str(ndpi_width)
print "height:".ljust(20) + str(ndpi_height)
print "level count:".ljust(20) + str(ndpi.level_count)


_red_sum    = 0.0
_total_sum  = 0.0

total_width  = ndpi.level_dimensions[level][0]
total_height = ndpi.level_dimensions[level][1]
print "split image {}x{} , level:{} , factor:{}".format(total_width,total_height,level,splitFactor)
bar = Bar('Processing', max=splitFactor**2)
for i in range(splitFactor):
	for j in range(splitFactor):
		x     = i * ndpi_width / splitFactor
		y     = j * ndpi_height / splitFactor
		w     = total_width / splitFactor
		h     = total_height / splitFactor

		if debug:
			print "\n>SLICE [{}][{}]".format(i,j)
			print "x:{:3} y:{:3} w:{:3}px h:{:3}px:".format(x,y,w,h)

		region  = ndpi.read_region((x,y), level, (w, h))
		
		red     = get_red(region)
		surface = get_surface(region)

		# Little hack.. because red, return 3 pixels... 

		_red_sum   += red.histogram()[-1]
		_total_sum += surface.histogram()[-1]

		if debug:
			print "found red {} and surface {}" .format(_red_sum, _total_sum)

		bar.next()

		
		# print "white:{}% black{}%".format(results["white"], results["black"])


bar.finish()
print "total red :".ljust(20) + str(_red_sum)
print "total surface:".ljust(20) + str(_total_sum)
print "Red percent:".ljust(20) + str(_red_sum / _total_sum * 100)




