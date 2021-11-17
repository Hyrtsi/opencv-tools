#!/usr/bin/env python3

import numpy as np
import cv2 as cv
import sys
from matplotlib import pyplot as plt

FILE_NAME = 'res/sunset.jpg'

def saturate(img):

	imghsv = cv.cvtColor(img, cv.COLOR_BGR2HSV).astype("float32")
	(h, s, v) = cv.split(imghsv)
	
	# 1.0 means no change. Under it converts to greyscale
	# and about 1.5 is immensely high 
	satadj = 999			
	s = s*satadj
	s = np.clip(s,0,255)
	imghsv = cv.merge([h,s,v])
	imgrgb = cv.cvtColor(imghsv.astype("uint8"), cv.COLOR_HSV2BGR)

	return imgrgb 

def analyze_image(img):
	channels = [0]
	mask = img
	color = ('b','g','r')
	for k,color in enumerate(color):
		histogram = cv.calcHist([img],[k],None,[256],[0,256])
		plt.plot(histogram, color = color)
		plt.xlim([0,256])
	plt.show()


# def draw_hist_2(img):
# 	hist = cv.calcHist([img],[0],None,[256],[0,256])
# 	plt.plot(hist)
# 	plt.show()



def draw_image(img):
	img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
	#cv.imshow('Display window', img)
	#key_input = cv.waitKey(0)
	plt.imshow(img)
	plt.show()

def main():
	print('hello world')
	
	# Display an image with opencv imshow

	img = cv.imread(cv.samples.findFile(FILE_NAME))

	if img is None:
		sys.exit('Could not read the image')

	img = saturate(img)
	draw_image(img)
	analyze_image(img)

	# img2 = plt.imread(FILE_NAME)
	# if img2 is None:
	# 	sys.exit('')
	# draw_hist_2(img2)



#####

if __name__ == "__main__":
	main()

###############

plt.ion()
class DynamicUpdate():
    #Suppose we know the x range
    min_x = 0
    max_x = 10

    def on_launch(self):
        #Set up plot
        self.figure, self.ax = plt.subplots()
        self.lines, = self.ax.plot([],[], 'o')
        #Autoscale on unknown axis and known lims on the other
        self.ax.set_autoscaley_on(True)
        self.ax.set_xlim(self.min_x, self.max_x)
        #Other stuff
        self.ax.grid()
        ...

    def on_running(self, xdata, ydata):
        #Update data (with the new _and_ the old points)
        self.lines.set_xdata(xdata)
        self.lines.set_ydata(ydata)
        #Need both of these in order to rescale
        self.ax.relim()
        self.ax.autoscale_view()
        #We need to draw *and* flush
        self.figure.canvas.draw()
        self.figure.canvas.flush_events()

    #Example
    def __call__(self):
        import numpy as np
        import time
        self.on_launch()
        xdata = []
        ydata = []
        for x in np.arange(0,1000,0.5):
            xdata.append(x)
            ydata.append(np.exp(-x**2)+10*np.exp(-(x-7)**2))
            self.on_running(xdata, ydata)
            time.sleep(0.1)
        return xdata, ydata

d = DynamicUpdate()
d()