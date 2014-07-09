import pygal
import detect_red
from progress.bar import Bar
import numpy as np

detect_red.run("exemple2.ndpi")

levelRange = range(2,7)
splitRange = range(3,10)

bar = Bar('Processing', max=max(splitRange))

bigdata  = list()

for level in levelRange:
	data = list()

	for split in splitRange:
		results = detect_red.run("exemple2.ndpi",split, level)
		
		red     = results["red"]
		total   = results["total"]
		
		print "red:{} total {}".format(red,total)

		percent = round(red / total * 100,4) 
		data.append(percent)

	bigdata.append(data)
		



bar.finish()


bar_chart = pygal.Bar()
bar_chart.title = 'Differents methods using detect_red cells'
np.array(splitRange) ** 2
bar_chart.x_labels = map(str, np.array(splitRange) ** 2)

index = 0

for level in levelRange:
	bar_chart.add("zoom {}".format(level), bigdata[index])
	index += 1


print bigdata
bar_chart.render_in_browser();
bar_chart.render_to_png("stat.png");
bar_chart.render_to_file("stat.svg");
