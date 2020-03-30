from time import *
from tkinter import *
from time import sleep

"""Depeyre Gatien"""

def mouv():
	global x
	if x > 750:
		x = 0
	else:
		x += 5
	can.coords(img, x, y)
	fen.after(500, mouv)

def block():
	global x
	print(x)
	fen.after(500, block)

fen = Tk()
fen.title("Mouvement d'une voiture")

can = Canvas(fen,bg="white", height=500, width=750)
can.grid()

x = 200
y = 250
fichierImg = PhotoImage(file="images/pion_blanc.png")
img = can.create_image(x, y, image=fichierImg)

mouv()
block()


fen.mainloop()




