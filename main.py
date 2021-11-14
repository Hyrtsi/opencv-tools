#!/usr/bin/env python3

import numpy as np
import cv2 as cv
import sys

def main():
	print('hello world')
	
	# Display an image with opencv imshow
	
	img = cv.imread(cv.samples.findFile('res/sunset.jpg'))

	if img is None:
		sys.exit('Could not read the image')

	cv.imshow('Display window', img)
	key_input = cv.waitKey(0)


#####

if __name__ == "__main__":
	main()