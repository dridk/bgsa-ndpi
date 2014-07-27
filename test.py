import bgsa
import Image 

img = Image.open("calibration/gland_89_9.jpg")

img.show()

bgsa.get_red(img).show()
bgsa.get_brown(img).show()