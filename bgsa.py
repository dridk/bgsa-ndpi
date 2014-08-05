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
from scipy.misc import *
from scipy.ndimage import morphology
from progress.bar import Bar
import colorsys
import time
import numpy as np
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
			pixel = ld[x,y]
			r = pixel[0]
			g = pixel[1]
			b = pixel[2]
			
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

def get_brown(source,brightness=-100  , contrast = 500, hue=-90, saturation=0.65):
	""" Return Brown composante""" 
	image        = source
	image        = shift_hue_saturation(image,hue,saturation)
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


def get_white_pixels(source):
	return source.histogram()[-1]





