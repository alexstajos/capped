import cv2
from Tkinter import *
from PIL import Image, ImageTk

class FrameCapped(Frame):
	FRAME_SKIP = 10
	def __init__(self, master=None):
		Frame.__init__(self, master)
		self.master = master
		self.frameIdx = 0
		self.pack(expand = True)
		self.init_vid_cap()
		self.create_image_grid()
		#self.after(0, func=lambda: self.update_all())

	def create_image_grid(self):
		self.imageGrid = []
		for i in range(0,2):
			print "loop%s" % i
			for j in range(0,3):
				idx = (i*3)+j
				print idx
				self.imageGrid.append(Label(master=self))
				self.imageGrid[idx].grid(row = i, column=j)
				self.set_frame_at_idx(self.imageGrid[i], self.FRAME_SKIP*idx)

	def set_frame_at_idx(self, imageLabel, idx):
		self.vidcap.set(cv2.cv.CV_CAP_PROP_POS_FRAMES, idx)
		success, image = self.vidcap.read()
		gray_im = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
		a = Image.fromarray(gray_im)
		b = ImageTk.PhotoImage(image=a)
		imageLabel.configure(image=b)
		imageLabel._image_cache = b  # avoid garbage collection

	def init_vid_cap(self):
		self.vidcap = cv2.VideoCapture("test.mp4")

	def update_all(self):
		self.update_frame()
		self.after(20, func=lambda: self.update_all())

	def update_frame(self):
		self.vidcap.set(cv2.cv.CV_CAP_PROP_POS_FRAMES, self.frameIdx)
		self.frameIdx += self.FRAME_SKIP
		success, image = self.vidcap.read()
		gray_im = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
		a = Image.fromarray(gray_im)
		b = ImageTk.PhotoImage(image=a)
		self.image_label.configure(image=b)
		self.image_label._image_cache = b  # avoid garbage collection
		self.update()

if __name__ == '__main__':
	root = Tk()
	capped = FrameCapped(root)
	capped.mainloop()