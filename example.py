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


def plt_hist(ax, img, color):
	colors = ['b', 'g', 'r']
	k = colors.index(color)
	histogram = cv.calcHist([img],[k],None,[256],[0,256])
	plt_handle, = ax.plot(histogram, color=color)
		# plt.xlim([0,256]) # necessary?

	return plt_handle

def main():
	fig, ax = plt.subplots(1, 2,figsize=(27.0,27.0))
	
	ax1 = ax[0] # The histogram
	ax2 = ax[1]	# The image

	ax2.set_xlim(0.0,1280.0)

	fig.suptitle('Saturation demo', fontsize=16)
	
	# Calculate the initial value for the image
	img = cv.imread(cv.samples.findFile(FILE_NAME))
	img = cv.cvtColor(img, cv.COLOR_BGR2RGB)

	# Draw the image
	# Take the handle for later
	imobj = ax2.imshow(img)

	# Axes for the saturation
	ax_sat = plt.axes([0.25, .03, 0.50, 0.02]) # location?

	# Slider
	sat_slider = Slider(ax_sat, 'Saturation', 0, 2, valinit=1)

	# Calculate the initial value for the histogram
	# TODO: rgb
	# TODO: make a function
	#histogram = cv.calcHist([img],[2],None,[256],[0,256])
	#hist_y, = ax1.plot(histogram, color='r')

	hist_y = plt_hist(ax1, img, 'r')

	def update(val):	
		newimg = img
		# update image
		newimg = saturate(newimg, sat_slider.val)
		imobj.set_data(newimg)

		# update also the histogram
		# TODO: use a function
		# TODO: rgb
		histogram = cv.calcHist([newimg],[2],None,[256],[0,256])
		hist_y.set_ydata(histogram)

		# redraw canvas while idle
		fig.canvas.draw_idle()

	# call update function on slider value change
	sat_slider.on_changed(update)

	plt.show()
	

main()