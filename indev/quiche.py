from tkinter import *

class Case(): #L'idée et de créer une fenêtre sans brodures mais qui apparaissent tout de même dans la barre de tâches
	def __init__(self, fen, i, j):
		self.i = i
		self.j = j
		width = (fen.canvas.winfo_width()-100)//8
		height = (fen.canvas.winfo_height()-100)//8
		self.canvas = Canvas(fen.canvas, bg=self.couleur_cases(), width=width, height=height, border=0, highlightthickness=0)
		self.id = fen.canvas.create_window(i*width, fen.canvas.winfo_height()-j*height, window=self.canvas, anchor=SW)
	def couleur_cases(self): #Définit si une case est noir ou blanche selon sa position
		if self.i%2 == 0 and self.j%2 == 0:
			return "black"
		elif self.i%2 != 0 and self.j%2 != 0:
			return "black"
		else:
			return "white"


def nouvelle_partie(fen, type):
	print(fen, type)
	afficher_plateau(fen)

def charger_partie(fen, fichier):
	print(fen, fichier)

def afficher_plateau(fen):
	fen.canvas.delete("all")
	for i in range(8):
		for j in range(8):
			fen.boutons_cases[tuple_to_string((i, j))] = Case(fen, i, j)

def tuple_to_string(a):
	return f"{a[0]}{a[1]}"