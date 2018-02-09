from Tkinter import *
from obj import *
import time

# This is a version of the tickertape, for just one listing. By listingID

x = sys.argv[1]


root = Tk()
delay = 100
v = StringVar()
label = Label(root, textvariable=v, height=5, width=40, font="Source\ Code\ Pro 12 bold", bg="NavajoWhite4")

v.set(Listing(x))
label.pack()
root.mainloop()	