from Tkinter import *
from obj import *
import time

root = Tk()
delay = 100
v = StringVar()
label = Label(root, textvariable=v, height=5, width=40, font="Source\ Code\ Pro 12 bold", bg="NavajoWhite4")

while True:
	for x in range(1,26):
		v.set(Listing(x))
		label.pack()
		root.update()
		time.sleep(5)
		continue	