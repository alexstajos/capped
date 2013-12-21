import cv2
from Tkinter import *
from PIL import Image, ImageTk

class FrameCapped(Frame):
	def __init__(self, master=None):
		Frame.__init__(self, master)
		self.master = master
		self.pack()
		self.create_widgets()
		self.init_vid_cap()
		self.after(0, func=lambda: self.update_all())

	def create_widgets(self):
		self.image_label = Label(master=self)
		self.image_label.pack()

	def init_vid_cap(self):
		self.vidcap = cv2.VideoCapture("test.mp4")

	def update_all(self):
		self.update_frame()
		self.after(20, func=lambda: self.update_all())

	def update_frame(self):
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