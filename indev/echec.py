from tkinter import *
from PIL import Image
from PIL import ImageTk

import classes
from classes import *

class Case():
	def __init__(self, fen, i, j):
		self.fen = fen
		self.i, self.j = i, j
		self.image_piece = None
		self.image_possibilite = None
		width = (fen.canvas.winfo_width()-100)//8
		height = (fen.canvas.winfo_height()-100)//8
		self.canvas = Canvas(fen.canvas, bg=self.couleur_cases(), width=width, height=height, border=0, highlightthickness=0)
		self.canvas.bind("<Button-1>", self.click)
		self.id = fen.canvas.create_window(j*width, fen.canvas.winfo_height()-i*height, window=self.canvas, anchor=SW)

	def couleur_cases(self): #Définit si une case est noir ou blanche selon sa position
		if self.i%2 == 0 and self.j%2 == 0:
			return self.fen.couleur_case_noire
		elif self.i%2 != 0 and self.j%2 != 0:
			return self.fen.couleur_case_noire
		else:
			return self.fen.couleur_case_blanche
	def placer_piece(self, piece):
		if self.image_piece != None:
			self.canvas.delete(self.image_piece)
			self.image_piece = None
		if piece == None:
			return
		self.image_piece = self.canvas.create_image(self.canvas.winfo_reqwidth()//2, self.canvas.winfo_reqheight()//2, image=piece.image)

	def possibilite(self, p):
		if self.image_possibilite != None:
			self.canvas.delete(self.image_possibilite)
			self.image_possibilite = None
		if p == True:
			size = 15
			self.image_possibilite = self.canvas.create_oval(self.canvas.winfo_reqwidth()//2-size, self.canvas.winfo_reqheight()//2-size, self.canvas.winfo_reqwidth()//2+size, self.canvas.winfo_reqheight()//2+size, fill="yelloW")


	def click(self, e):
		fen = self.fen
		i, j = self.i, self.j
		if fen.partie["possibilites"] == []:
			if fen.partie["plateau"][tuple_to_string((i, j))] != None and fen.partie["plateau"][tuple_to_string((i, j))].equipe == fen.partie["joueur"]:
				fen.partie["possibilites"] = fen.partie["plateau"][tuple_to_string((i, j))].cases_possibles(fen.partie["plateau"])
				fen.partie["actif"] = fen.partie["plateau"][tuple_to_string((i, j))]
		else:
			if tuple_to_string((i, j)) in fen.partie["possibilites"]:
				fen.partie["possibilites"] = []
				deplacer(fen, fen.partie["actif"], i, j)
				passer_tour(fen)
				fen.partie["actif"] = None
			else:
				if fen.partie["plateau"][tuple_to_string((i, j))] != None and fen.partie["plateau"][
					tuple_to_string((i, j))].equipe == fen.partie["joueur"]:
					fen.partie["possibilites"] = fen.partie["plateau"][f'{i}{j}'].cases_possibles(fen.partie["plateau"])
					fen.partie["actif"] = fen.partie["plateau"][f'{i}{j}']
				else:
					fen.partie["possibilites"] = []
					fen.partie["actif"] = None
		afficher_possibilites(fen)



"""Fonctions de parties"""
def nouvelle_partie(fen, type):
	fen.partie = {}
	fen.partie["type"] = type
	fen.partie["plateau"] = creer_plateau()
	fen.partie["actif"] = None
	fen.partie["possibilites"] = []
	fen.partie["joueur"] = "blanc"
	afficher_plateau(fen, fen.partie["plateau"])

def charger_partie(fen, fichier):
	print(fen, fichier)

"""Création du plateau"""
def creer_plateau():
	plateau = {}
	for i in range(8):
		for j in range(8):
			plateau[tuple_to_string((i, j))] = None
	initialiser_pieces(plateau)
	return plateau

def initialiser_pieces(plateau):
	for i in range(8):
		# Placement des pions
		pion = Pion("blanc", 1, i)
		plateau[f'{1}{i}'] = pion
		pion = Pion("noir", 6, i)
		plateau[f'{6}{i}'] = pion

	for i in range(2):
		# Placement des tours
		plateau[f'{0}{i * 7}'] = Tour("blanc", 0, i * 7)
		plateau[f'{7}{i * 7}'] = Tour("noir", 7, i * 7)

		# Placement des cavaliers
		plateau[f'{0}{1 + i * 5}'] = Cavalier("blanc", 0, 1 + i * 5)
		plateau[f'{7}{1 + i * 5}'] = Cavalier("noir", 7, 1 + i * 5)

		# Placement des fous
		plateau[f'{0}{2 + i * 3}'] = Fou("blanc", 0, 2 + i * 3)
		plateau[f'{7}{2 + i * 3}'] = Fou("noir", 7, 2 + i * 3)

	# Dames et Rois
	plateau[f'{0}{4}'] = Roi("blanc", 0, 4)
	plateau[f'{7}{3}'] = Roi("noir", 7, 3)
	plateau[f'{0}{3}'] = Dame("blanc", 0, 3)
	plateau[f'{7}{4}'] = Dame("noir", 7, 4)


"""Fonctions utilitaires"""
def tuple_to_string(a):
	return f"{a[0]}{a[1]}"

def obtenir_image(chemin):
	img = Image.open(chemin)
	img = img.resize((40, 40))
	photoImg = ImageTk.PhotoImage(img)
	return photoImg

def case_hors_plateau(coord):
	i=coord[0]
	j=coord[1]
	if i < 0 or i>7 or j<0 or j>7:
		return True
	else:
		return False


"""Gestion des parties"""
def sauvegarde_partie(nom, plateau, joueur):
	with open("parties/" + nom, "w") as fichier:
		fichier.write(joueur + "\n")
		for i in range(8):
			ligne = ""
			for j in range(8):
				if plateau[tuple_to_string((i, j))] == None:
					ligne += "N"
				else:
					ligne += plateau[tuple_to_string((i, j))].lettre
			ligne += "\n"
			fichier.write(ligne)


"""Fonctions de jeu"""
def deplacer(fen, piece, i, j):
	i0, j0 = piece.i, piece.j
	fen.partie["plateau"][tuple_to_string((i0, j0))] = None
	if type(piece) == classes.Pion: #Promotion
		if i == 0 or i == 7:
			piece = classes.Dame(piece.equipe, i, j)
	fen.partie["plateau"][tuple_to_string((i, j))] = piece
	piece.deplace = True
	fen.boutons_cases[tuple_to_string((i0, j0))].placer_piece(fen.partie["plateau"][tuple_to_string((i0, j0))])
	fen.boutons_cases[tuple_to_string((i, j))].placer_piece(fen.partie["plateau"][tuple_to_string((i, j))])
	piece.i, piece.j = i, j

def passer_tour(fen):
	if fen.partie["joueur"] == "blanc":
		fen.partie["joueur"] = "noir"
	else:
		fen.partie["joueur"] = "blanc"


"""Fonctions d'affichage"""
def afficher_plateau(fen, plateau):
	fen.canvas.delete("all")
	for i in range(8):
		for j in range(8):
			fen.boutons_cases[tuple_to_string((i, j))] = Case(fen, i, j)
			fen.boutons_cases[tuple_to_string((i, j))].placer_piece(plateau[tuple_to_string((i, j))])

def afficher_possibilites(fen):
	for case in fen.partie["plateau"]:
		if case in fen.partie["possibilites"]:
			fen.boutons_cases[case].possibilite(True)
		else:
			fen.boutons_cases[case].possibilite(False)
