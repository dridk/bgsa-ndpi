from openslide import *
from argparse import ArgumentParser
import ImageEnhance
import ImageOps
import ImageStat
import time
import numpy as np
from scipy.ndimage import morphology
from progress.bar import Bar
import time
import os

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


def run(filename, split=2, level=4, debug=False):

# Create OpenSlide object
	ndpi         = OpenSlide(filename)
	ndpi_width   = ndpi.dimensions[0]
	ndpi_height  = ndpi.dimensions[1]
	total_width  = ndpi.level_dimensions[level][0]
	total_height = ndpi.level_dimensions[level][1]
	_red_sum     = 0.0
	_total_sum   = 0.0
	startTime    = time.time()

	if debug:
		print "================ START ================="
		print "LOAD {}".format(filename)
		print "width:".ljust(20) + str(ndpi_width)
		print "height:".ljust(20) + str(ndpi_height)
		print "level count:".ljust(20) + str(ndpi.level_count)
		print "split image {}x{} , level:{} , factor:{}".format(total_width,total_height,level,split)
		
	bar = Bar('Processing', max=split**2)
	for i in range(split):
		for j in range(split):
			x     = i * ndpi_width / split
			y     = j * ndpi_height / split
			w     = total_width / split
			h     = total_height / split

			if debug:
				print "\n>SLICE [{}][{}]".format(i,j)
				print "x:{:3} y:{:3} w:{:3}px h:{:3}px:".format(x,y,w,h)

			region  = ndpi.read_region((x,y), level, (w, h))
			
			red     = get_red(region)
			surface = get_surface(region)

			region.save("output/normal_slice{}{}.png".format(i,j))
			red.save("output/red_slice_{}{}.png".format(i,j))
			surface.save("output/total_slice_{}{}.png".format(i,j))

			# Little hack.. because red, return 3 pixels... 

			_red_sum   += red.histogram()[-1]
			_total_sum += surface.histogram()[-1]

			if debug:
				print "found red {} and surface {}" .format(_red_sum, _total_sum)
				bar.next()

			
			# print "white:{}% black{}%".format(results["white"], results["black"])


	
	if debug:
		bar.finish()
		print "Finished....in {:.2f} sec".format(time.time() - startTime)
		print "total red :".ljust(20) + str(_red_sum)
		print "total surface:".ljust(20) + str(_total_sum)
		print "Red percent:".ljust(20) + str(_red_sum / _total_sum * 100)

	return {"red":_red_sum,"total": _total_sum}






# ========== Main ===================================

# Settings arguments parser 
if __name__ == '__main__':
	parser = ArgumentParser(description="compute a ndpi file")
	parser.add_argument("filename")
	parser.add_argument("-s", "--split", default=2,  type=int)
	parser.add_argument("-l", "--level", default=4,  type=int)
	#parser.add_argument("-t", "--target", default="output",  type=int)
	parser.add_argument("-d", "--debug", default=False,  type=bool)

	args = parser.parse_args()
	
	try:
		os.mkdir("output")
	except:
		print("output already exists")

	run(args.filename, args.split, args.level, args.debug)


