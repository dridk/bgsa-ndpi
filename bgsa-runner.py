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

import bgsa
from openslide import OpenSlide
from progress.bar import Bar
from argparse import ArgumentParser
import time
import os

def run(filename, split, level, dred, dbrown, debug):

# Create OpenSlide object
	ndpi         = OpenSlide(filename)
	ndpi_width   = ndpi.dimensions[0]
	ndpi_height  = ndpi.dimensions[1]
	total_width  = ndpi.level_dimensions[level][0]
	total_height = ndpi.level_dimensions[level][1]
	
	red_sum     = 0.0

	startTime    = time.time()


	print "filename: {}".format(filename)
	print "split: {}".format(split)
	print "level: {}".format(level)
	print "dred: {}".format(dred)
	print "dbrown: {}".format(dbrown)
	print "debug: {}".format(debug)





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
			red     = bgsa.get_red(region, brightness=-dred)
			# brown   = get_brown(region)

			region.save("output/normal_slice{}{}.png".format(i,j))
			red.save("output/red_slice_{}{}.png".format(i,j))
			

			red_sum   += bgsa.get_white_pixels(red)

			if debug:
				print "found red: {}" .format(red_sum)
				bar.next()

			
			# print "white:{}% black{}%".format(results["white"], results["black"])

	if debug:
		bar.finish()
		print "Finished....in {:.2f} sec".format(time.time() - startTime)
		print "total red :".ljust(20) + str(red_sum)

	return {"red":red_sum}






# ========== Main ===================================



# Settings arguments parser 
if __name__ == '__main__':
	parser = ArgumentParser(description="compute a ndpi file")
	parser.add_argument("filename")
	parser.add_argument("-s", "--split", default=2,  type=int)
	parser.add_argument("-z", "--zoom", default=4,  type=int)
	parser.add_argument("-r", "--red", default=50,  type=int)
	parser.add_argument("-b", "--brown", default=4,  type=int)
	parser.add_argument("-d", "--debug", default=False,  type=bool)


	args = parser.parse_args()
	
	try:
		os.mkdir("output")
	except:
		print("output already exists")

	run(args.filename, args.split, args.zoom,args.red, args.brown, args.debug)







