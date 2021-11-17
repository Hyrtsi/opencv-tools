import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.widgets import Slider
import cv2 as cv

FILE_NAME = 'res/sunset.jpg'

# https://matplotlib.org/3.3.1/gallery/widgets/slider_demo.html
# https://sodocumentation.net/matplotlib/topic/6983/animations-and-interactive-plotting

# img:
# image in opencv format
#
# satadj:
# 1.0 means no change. Under it converts to greyscale
# and about 1.5 is immensely high 
def saturate(img, satadj):

	imghsv = cv.cvtColor(img, cv.COLOR_BGR2HSV).astype("float32")
	(h, s, v) = cv.split(imghsv)
	

	s = s*satadj
	s = np.clip(s,0,255)
	imghsv = cv.merge([h,s,v])
	imgrgb = cv.cvtColor(imghsv.astype("uint8"), cv.COLOR_HSV2BGR)

	return imgrgb 


def main():
	fig, ax = plt.subplots()
	fig.suptitle('Saturation demo', fontsize=16)
	
	img = cv.imread(cv.samples.findFile(FILE_NAME))
	img = cv.cvtColor(img, cv.COLOR_BGR2RGB)


	imobj = plt.imshow(img)
	axamp = plt.axes([0.25, .03, 0.50, 0.02]) # location?

	# Slider
	initial_amp = .5
	samp = Slider(axamp, 'Saturation', 0, 2, valinit=initial_amp)

	def update(val):
		# amp is the current value of the slider
		amp = samp.val
		
		newimg = img
		# update image
		newimg = saturate(newimg, samp.val)
		imobj.set_data(newimg)

		# redraw canvas while idle
		fig.canvas.draw_idle()

	# call update function on slider value change
	samp.on_changed(update)

	plt.show()
	

main()