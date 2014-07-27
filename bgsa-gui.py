import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import * 
import bgsa
from PIL import Image
import ImageQt

class Editor(QWidget):
	def __init__(self, parent = None):
		super(Editor,self).__init__(parent)
		self.originalPix 	= QLabel("original");
		self.transformPix 	= QLabel("transformed");
		self.spinbox       	= QSpinBox()
		self.button         = QPushButton("test")
		layout 			    = QVBoxLayout()

		layout.addWidget(self.originalPix)
		layout.addWidget(self.transformPix)
		layout.addWidget(self.spinbox)
		layout.addWidget(self.button)
		self.setLayout(layout)
		self.resize(800,600)

		self.spinbox.valueChanged.connect(self.analyse)
		self.button.clicked.connect(self.analyse)

	def loadImage(self, filename):
		self.filename = filename
		# self.originalPix.setPixmap(QPixmap(filename).scaledToWidth(500))

	def analyse(self, value=1):
		img = Image.open(self.filename)
		img = bgsa.get_red(img, -value*10)

		# image = img.copy(0,0, img.width(), img.height())
		img = ImageQt.ImageQt(img).copy()
		pix = QPixmap.fromImage(img)
		

		self.originalPix.setPixmap(pix)













app = QApplication(sys.argv)

e = Editor()
e.loadImage("calibration/gland_89_0.jpg")
e.show()


app.exec_()
sys.exit()