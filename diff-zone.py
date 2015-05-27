import cv2
import numpy as py


class DiffZone(object):
	def __init__(self):
		self.min_x = 480
		self.min_y = 743
		self.max_x = 0
		self.max_y = 0


def compare_pixel(px):
	if px[0] == 0 and px[1] == 0 and px[2] == 0 :
		return False
	else :
		return True

def compare_rect(rect,x,y):
	if x > rect.max_x:
		rect.max_x = x
	elif x < rect.min_x:
		rect.min_x = x

	if y > rect.max_y:
		rect.max_y = y
	elif y < rect.min_y:
		rect.min_y = y

def find_diff_rect(img):
	#initial rect
	rect = DiffZone()

	#find rect
	height = img.shape[0]
	width = img.shape[1]
	for j in range(height):
		for i in range(width):
			px = img[j,i]
			if compare_pixel(px) :
				compare_rect(rect,i,j)

	print rect.min_x
	print rect.min_y
	print rect.max_x
	print rect.max_y

img = cv2.imread('3.png')
find_diff_rect(img)
