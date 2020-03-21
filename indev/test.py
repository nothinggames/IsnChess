import tkinter as Tkinter

from tkinter import *

class NoBorderWindow(Tk):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.little = Tk()
		self.little.geometry("0x0")
		self.little.lift(aboveThis=self)
		self.little.bind("<Map>", self.apparition)
		self.little.bind("<Unmap>", self.disparition)
		self.little.protocol("WM_DELETE_WINDOW", self.quit)
		self.overrideredirect(True)
		self.lift()
		self.attributes('-topmost', True)

		self.background_image = PhotoImage(file="background.png")
		menu = Canvas(self, border=-5, background="black", width=self.background_image.width(), height=self.background_image.height())
		menu.create_image(0, 0, image=self.background_image, anchor=NW)
		menu.grid(row=1, column=0)

		centrer_fenetre(self.little)
		centrer_fenetre(self)

		self.bouton_fermer = Button(self, bg="#802812", text="X", fg="white", border=5, relief=SUNKEN, command=self.quit)
		self.bouton_fermer.grid(row=0, column=0)


	def apparition(self, e):
		self.wm_deiconify()
		self.lift()
	def disparition(self, e):
		self.wm_withdraw()
		self.lift()

def centrer_fenetre(fen):
	fen.update_idletasks()
	width = fen.winfo_width()
	height = fen.winfo_height()
	x = (fen.winfo_screenwidth() // 2) - (width // 2)
	y = (fen.winfo_screenheight() // 2) - (height // 2)
	fen.geometry('{}x{}+{}+{}'.format(width, height, x, y))


app = NoBorderWindow()
app.little.title("Chesscraft")
app.mainloop()