#!/usr/bin/env python3

import numpy as np
import cv2 as cv
import sys
from matplotlib import pyplot as plt

FILE_NAME = 'res/cat.png' #'res/red.png'
# 'res/sunset.jpg'

def saturate(img):
	return img # * img

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
	cv.imshow('Display window', img)
	key_input = cv.waitKey(0)


def main():
	print('hello world')
	
	# Display an image with opencv imshow

	img = cv.imread(cv.samples.findFile(FILE_NAME))

	if img is None:
		sys.exit('Could not read the image')

	img = saturate(img)
	# draw_image(img)
	analyze_image(img)

	# img2 = plt.imread(FILE_NAME)
	# if img2 is None:
	# 	sys.exit('')
	# draw_hist_2(img2)



#####

if __name__ == "__main__":
	main()