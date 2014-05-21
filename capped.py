import cv2
from Tkinter import *
import numpy as np
from PIL import Image, ImageTk
import math

class FrameCapped(Frame):
	ROWS = 3
	COLS = 3
	def __init__(self, master=None):
		Frame.__init__(self, master)
		self.master = master
		self.frameIdx = 0
		self.pack(expand = True)
		self.init_vid_cap()
		self.create_image_grid(0, self.totalFrames())

	def onClick(self, startCnt, idx, skipAmt):
		 newStart = startCnt + (idx*skipAmt)
		 newEnd = newStart + skipAmt
		 self.create_image_grid(newStart, newEnd)
		 self.update()

	def create_image_grid(self, startCnt, endIdx):
		print "Start: %d" % startCnt
		print "End: %d" % endIdx
		self.FRAME_SKIP =  math.floor((endIdx - startCnt)/(self.ROWS * self.COLS))
		print "Skip: %d" % self.FRAME_SKIP
		self.imageGrid = []
		for i in range(self.ROWS):
			for j in range(self.COLS):
				idx = (i*self.COLS)+j
				self.imageGrid.append(Label(master=self, borderwidth = 3))
				self.imageGrid[idx].grid(row = i, column=j)
				self.imageGrid[idx].bind("<Button-1>", lambda e, startCnt = startCnt, idx=idx, skipAmt = self.FRAME_SKIP:self.onClick(startCnt, idx, skipAmt))
				self.set_frame_at_idx(self.imageGrid[idx], startCnt + self.FRAME_SKIP*idx)

	def set_frame_at_idx(self, imageLabel, idx):
		print "Frame: %d" % idx
		self.vidcap.set(cv2.cv.CV_CAP_PROP_POS_FRAMES, idx)
		success, image = self.vidcap.read()
		image = self.scaleImageToSize(image, 200)

		gray_im = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
		a = Image.fromarray(gray_im)
		b = ImageTk.PhotoImage(image=a)
		imageLabel.configure(image=b)
		imageLabel._image_cache = b  # avoid garbage collection

	def init_vid_cap(self):
		#self.vidcap = cv2.VideoCapture("test.mp4")
		self.vidcap = cv2.VideoCapture("bigTest.avi")

	def totalFrames(self):
		return self.vidcap.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT)

	def scaleImageToSize(self, image, dstWidth):
		height, width = image.shape[:2]
		ratio = dstWidth/float(width)

		return cv2.resize(image, (int(width*ratio), int(height*ratio)))



if __name__ == '__main__':
	root = Tk()
	capped = FrameCapped(root)
	capped.mainloop()