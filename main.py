import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.widgets import Slider
import cv2 as cv

FILE_NAME = 'res/mountain-and-lake.jpg'

# https://matplotlib.org/3.3.1/gallery/widgets/slider_demo.html
# https://sodocumentation.net/matplotlib/topic/6983/animations-and-interactive-plotting


# img:
# image in rbg
#
# satadj:
# 1.0 means no change. Under it converts to greyscale
# and about 1.5 is immensely high 
def saturate(img, satadj):
	imghsv = cv.cvtColor(img, cv.COLOR_RGB2HSV).astype("float32")
	(h, s, v) = cv.split(imghsv)
	
	s = s*satadj
	s = np.clip(s,0,255)
	imghsv = cv.merge([h,s,v])
	imgrgb = cv.cvtColor(imghsv.astype("uint8"), cv.COLOR_HSV2RGB)

	# assume: return rgb
	return imgrgb 


def brightness(img, exp_adj):
	imghsv = cv.cvtColor(img, cv.COLOR_RGB2HSV).astype("float32")
	(h, s, v) = cv.split(imghsv)
	
	v = v*exp_adj
	v = np.clip(v,0,255)
	imghsv = cv.merge([h,s,v])
	imgrgb = cv.cvtColor(imghsv.astype("uint8"), cv.COLOR_HSV2RGB)

	# assume: return rgb
	return imgrgb 

def plt_hist(ax, img, color):
	colors = ['b', 'g', 'r']
	k = colors.index(color)
	histogram = cv.calcHist([img],[k],None,[256],[0,256])
	plt_handle, = ax.plot(histogram, color=color)

	return plt_handle

def main():
	fig, ax = plt.subplots(1, 2,figsize=(27.0,27.0))
	
	ax1 = ax[0] # The histogram
	ax2 = ax[1]	# The image

	ax2.set_xlim(0.0,1280.0)

	fig.suptitle('Image toner', fontsize=16)
	
	# Calculate the initial value for the image
	img = cv.imread(cv.samples.findFile(FILE_NAME)) # assume: BGR
	img = cv.cvtColor(img, cv.COLOR_BGR2RGB) # plt assumes RGB

	# Draw the image
	# Take the handle for later
	imobj = ax2.imshow(img)

	# Axes for the saturation and brightness
	ax_sat = plt.axes([0.25, .03, 0.50, 0.02])
	ax_exp = plt.axes([0.25, 0.01, 0.50, 0.02])

	# Slider
	sat_slider = Slider(ax_sat, 'Saturation', 0, 20, valinit=1)
	exp_slider = Slider(ax_exp, 'Brightness', -10, 10, valinit=1)

	# Histogram
	colors = ('r', 'g', 'b')
	lines = []
	for k,color in enumerate(colors):
		histogram = cv.calcHist([img],[k],None,[256],[0,256])
		line, = ax1.plot(histogram,color=color)
		lines.append(line)

	def update_sat(val):	
		newimg = img
		# update image
		newimg = saturate(newimg, sat_slider.val)
		newimg = brightness(newimg,val)

		imobj.set_data(newimg)

		# update also the histogram

		colors = ('r', 'g', 'b')
		for k,color in enumerate(colors):
			histogram = cv.calcHist([newimg],[k],None,[256],[0,256])
			lines[k].set_ydata(histogram)



		# redraw canvas while idle
		fig.canvas.draw_idle()

	def update_exp(val):
		newimg = img
		newimg = saturate(newimg, sat_slider.val)
		newimg = brightness(newimg,val)
		imobj.set_data(newimg)

		# update also the histogram

		colors = ('b', 'g', 'r')
		for k,color in enumerate(colors):
			histogram = cv.calcHist([newimg],[k],None,[256],[0,256])
			lines[k].set_ydata(histogram)

		# redraw canvas while idle
		fig.canvas.draw_idle()

	# call update function on slider value change
	sat_slider.on_changed(update_sat)
	exp_slider.on_changed(update_exp)


	plt.show()
	

main()