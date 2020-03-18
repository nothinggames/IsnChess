from tkinter import *
from PIL import Image
from PIL import ImageTk


<<<<<<< HEAD
# ------------------------ceci est la partie affichege---------------------------

def actualiser(plateau, buttons_cases):  # Vérifie toutes les cases du plateau en affichant les pièces (ou les vides). (Va possiblement être transformée
=======

#------------------------ceci est la partie affichege---------------------------

def actualiser(plateau, buttons_cases): #Vérifie toutes les cases du plateau en affichant les pièces (ou les vides). (Va possiblement être transformée
>>>>>>> 7b6dd16fff55fae8d10e2b39e095fa98cccb6b32
	# en une fonction qui ne change que la case demandée afin de ne pas avoir à parcourir tout le plateau lors d'un mouvement.
	for e in plateau:
		if plateau[e] != None:
			buttons_cases[e].changer_image(plateau[e].image)
		else:
			buttons_cases[e].changer_image("")
		buttons_cases[e].bouton["bg"] = buttons_cases[e].couleur_cases()

<<<<<<< HEAD

=======
>>>>>>> 7b6dd16fff55fae8d10e2b39e095fa98cccb6b32
def actualiser_deux_pieces(plateau, buttons_cases, i1, j1, p2):
	buttons_cases[f"{i1}{j1}"].changer_image("")
	buttons_cases[f"{p2.i}{p2.j}"].changer_image(plateau[f'{p2.i}{p2.j}'].image)

<<<<<<< HEAD

=======
>>>>>>> 7b6dd16fff55fae8d10e2b39e095fa98cccb6b32
def actualier_couleurs(buttons_cases, possibilites):
	for case in buttons_cases:
		if case in possibilites:
			buttons_cases[case].bouton["bg"] = "yellow"
		else:
			buttons_cases[case].bouton["bg"] = buttons_cases[case].couleur_cases()


<<<<<<< HEAD
=======

>>>>>>> 7b6dd16fff55fae8d10e2b39e095fa98cccb6b32
def obtenir_image(chemin):
	img = Image.open(chemin)
	img = img.resize((50, 50))
	photoImg = ImageTk.PhotoImage(img)
	return photoImg
<<<<<<< HEAD
	print("*")


def deplacer(plateau, buttons_cases, piece, i, j):
	i0, j0 = piece.i, piece.j
	plateau[f'{piece.i}{piece.j}'] = None  # Vide la case d'ou la pièce part
	piece.i = i
	piece.j = j
	piece.deplace = True
	plateau[f'{i}{j}'] = piece  # Met la pièce à sa nouvelle coodonnée
	actualiser_deux_pieces(plateau, buttons_cases, i0, j0, piece)
	actualier_couleurs(buttons_cases, [])


def case_hors_plateau(coord):
	i = coord[0]
	j = coord[1]
	if i < 0 or i > 7 or j < 0 or j > 7:
=======

def deplacer(plateau, buttons_cases, piece, i, j):
	i0, j0 = piece.i, piece.j
	plateau[f'{piece.i}{piece.j}'] = None #Vide la case d'ou la pièce part
	piece.i = i
	piece.j = j
	piece.deplace = True
	plateau[f'{i}{j}'] = piece #Met la pièce à sa nouvelle coodonnée
	actualiser_deux_pieces(plateau, buttons_cases, i0, j0, piece)
	actualier_couleurs(buttons_cases, [])
    

def case_hors_plateau(coord):
	i=coord[0]
	j=coord[1]
	if i < 0 or i>7 or j<0 or j>7:
>>>>>>> 7b6dd16fff55fae8d10e2b39e095fa98cccb6b32
		return True
	else:
		return False

<<<<<<< HEAD

=======
>>>>>>> 7b6dd16fff55fae8d10e2b39e095fa98cccb6b32
def tuple_to_string(a):
	return f"{a[0]}{a[1]}"


<<<<<<< HEAD
def est_echec(plateau):
	for e in plateau:
		print(e)  # plateau[f'{self.i+a}{self.j}']
=======




def est_echec(plateau):
	for e in plateau:
		print(e)#plateau[f'{self.i+a}{self.j}']
>>>>>>> 7b6dd16fff55fae8d10e2b39e095fa98cccb6b32
