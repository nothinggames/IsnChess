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

		self.barre_outils = Frame(self, background="#3b3838")
		self.barre_outils.grid(row=0, column=0,)

		#self.bouton_reduire = Button(self.barre_outils, bg="#960d03", text="-", fg="white", border=0, relief=SUNKEN, command=self.little.iconify)
		#self.bouton_reduire.grid(row=0, column=0)

		self.bouton_reduire = Button(self.barre_outils, width=3, height=1, bg="#3b3838", activebackground="#292626", text="-", font="Helvetica 10 bold", fg="white", border=0, relief=SUNKEN, command=self.little.iconify)
		self.bouton_reduire.grid(row=0, column=1)
		self.bouton_fermer = Button(self.barre_outils, width=3, height=1, bg="#960d03", activebackground="#6e0a02", text="x", font="Helvetica 10 bold", fg="white", border=0, relief=SUNKEN, command=self.quit)
		self.bouton_fermer.grid(row=0, column=2)
		self.barre_outils_vide = Canvas(self.barre_outils, width=self.background_image.width()-40-30, height=0, background=self.barre_outils["bg"], border=-5).grid(row=0, column=0)

		self.bouton_reduire.bind("<Enter>", self.entree_bouton)
		self.bouton_reduire.bind("<Leave>", self.sortie_bouton)
		self.bouton_fermer.bind("<Enter>", self.entree_bouton)
		self.bouton_fermer.bind("<Leave>", self.sortie_bouton)

	def apparition(self, e):
		self.wm_deiconify()
		self.lift()
	def disparition(self, e):
		self.wm_withdraw()
		self.lift()

	def entree_bouton(self, e):
		e.widget["bg"] = e.widget["activebackground"]
	def sortie_bouton(self, e):
		color = None
		if e.widget == self.bouton_fermer:
			color = "#960d03"
		if e.widget == self.bouton_reduire:
			color = "#3b3838"
		if color != None:
			e.widget["bg"] = color


def centrer_fenetre(fen):
	fen.update_idletasks()
	width = fen.winfo_width()
	height = fen.winfo_height()
	x = (fen.winfo_screenwidth() // 2) - (width // 2)
	y = (fen.winfo_screenheight() // 2) - (height // 2)
	fen.geometry('{}x{}+{}+{}'.format(width, height, x, y))

def changer_couleur_bouton(bouton, couleur):
	bouton["bg"] = couleur

app = NoBorderWindow()
app.little.title("Chesscraft")
app.mainloop()