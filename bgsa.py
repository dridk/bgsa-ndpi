 #!/usr/bin/python
 # This program is free software: you can redistribute it and/or modify
 # it under the terms of the GNU General Public License as published by
 #the Free Software Foundation, either version 3 of the License, or
 #(at your option) any later version.

 #This program is distributed in the hope that it will be useful,
 #but WITHOUT ANY WARRANTY; without even the implied warranty of
 #MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 #GNU General Public License for more details.

 #You should have received a copy of the GNU General Public License
 #along with this program.  If not, see <http://www.gnu.org/licenses/>.

__author__ = 'Sacha Schutz'
__version__ = (1, 2, 0)
__license__ = 'GPL3'



from openslide import *
from argparse import ArgumentParser
import colorsys
from scipy.misc import *

import time
import numpy as np
from scipy.ndimage import morphology
from progress.bar import Bar
import time
import os

# ========== FUNCTION ===================================
def shift_hue_saturation(image, hue = -90, saturation = 0.65):
	""" Rotate hue and set the contrast""" 
	copy = image.copy()
	ld = copy.load()
	width, height = copy.size
	for y in range(height):
		for x in range(width):
			r,g,b = ld[x,y]
			h,s,v = colorsys.rgb_to_hsv(r/255., g/255., b/255.)
			h = (h + hue/360.0) % 1.0
			s = s**saturation
			r,g,b = colorsys.hsv_to_rgb(h, s, v)
			ld[x,y] = (int(r * 255.9999), int(g * 255.9999), int(b * 255.9999))
	return copy

def shift_brightness_contrast(image, brightness=-100, contrast=300):
	""" Shift contrast and brightness""" 
	def vect(a):
		c   = contrast
		b   = 100 * brightness
		res = ((a - 127.5) * c + 127.5) + b
		if res <0 :
			return 0
		if res > 255:
			return 255
		return res
	
	transform = np.vectorize(vect)
	data = transform(fromimage(image)).astype(np.uint8)
	return toimage(data)


def get_red(source, brightness=-150, contrast = 500):
	""" Return Red composante""" 
	image        = source.convert("YCbCr")
	layer        = image.split()[2];
	layer 		 = shift_brightness_contrast(layer,brightness,contrast)
	return layer

def get_brown(source,brightness=-100, contrast = 500, hue=-90, saturation=0.65):
	""" Return Brown composante""" 
	image        = source
	image        = shift_hue_saturation(image,hue,saturation)
	image.show()
	image        = image.convert("YCbCr")
	layer        = image.split()[2];
	layer        = shift_brightness_contrast(layer,brightness,contrast)

	return layer

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
			# brown   = get_brown(region)
			surface = get_surface(region)

			region.save("output/normal_slice{}{}.png".format(i,j))
			red.save("output/red_slice_{}{}.png".format(i,j))
			# brown.save("output/red_slice_{}{}.png".format(i,j))
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

