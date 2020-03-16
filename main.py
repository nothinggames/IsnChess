from tkinter import *


"""Pour redefinir la taille d'une image, il faut utiliser Image.resize((myWidth,myHeight))"""

class Bouton():#Cette classe sert à créer et stocker chaque bouton avec ses coordonnées (O, i, j). O est situé en bas à gauche de la fenetre
	def __init__(self, i, j, frame_plateau):
		self.i = i #i correspond au numéro de la ligne
		self.j = j #j correspond au numéro de la colone
		self.bouton = Button(frame_plateau, background=self.couleur_cases(), command=lambda: appel_bouton(self.i, self.j),
						padx=30, pady=30, image="", bd=5) #Chaque case est un bouton qui appel la fonction appel_bouton(i, j)
		self.bouton_grid()

	def changer_image(self, img): #Sert à modifier l'image à afficher lors du placement des pièces ou lors d'un déplacement.
		self.bouton["image"] = img #On modifie l'attribut image de notre bouton.


	def couleur_cases(self): #Définit si une case est noir ou blanche selon sa position
		if self.i%2 == 0 and self.j%2 == 0:
			return "black"
		elif self.i%2 != 0 and self.j%2 != 0:
			return "black"
		else:
			return "white"

	def bouton_grid(self): #affiche le bouton.
		self.bouton.grid(row=8-self.i, column=self.j)



def actualiser(): #Vérifie toutes les cases du plateau en affichant les pièces (ou les vides). (Va possiblement être transformée
	# en une fonction qui ne change que la case demandée afin de ne pas avoir à parcourir tout le plateau lors d'un mouvement.
	for e in plateau:
		if plateau[e] != None:
			buttons_cases[e].changer_image(plateau[e].image)
		else:
			buttons_cases[e].changer_image("")


def actualiser_deux_pieces(i1, j1, p2):
	buttons_cases[f"{i1}{j1}"].changer_image("")
	buttons_cases[f"{p2.i}{p2.j}"].changer_image(plateau[f'{p2.i}{p2.j}'].image)
	print("ok")

def creation_terrain(): #inicialise le plateau.
	frame_plateau = Frame(fen) #La frame qui contient les boutons
	buttons_cases = {} #Un dictionnaire qui renvoie le bouton correspondant aux coordonnées ["ij"]
	plateau = {} #Le plateau contion les pièces et les vides, il sera mit dans un fichier externe afin de sauvegarder les parties. (Les pièces sont des class)
	for i in range(8):
		for j in range(8):
			buttons_cases[f'{i}{j}'] = Bouton(i, j, frame_plateau) #Création des boutons
			plateau[f'{i}{j}'] = None #Création d'un plateau vide
	frame_plateau.grid(row=0, column=0)
	return buttons_cases, plateau


def appel_bouton(i, j): #Fonction appelé lors d'un clic sur un bouton, les coordonnées (i, j) donnent le bouton activé
	print(plateau[f'{i}{j}'])
	global actif, possibilite
	if possibilite == None:
		if plateau[f'{i}{j}'] != None:
			possibilite = plateau[f'{i}{j}'].cases_possibles(plateau)
			actif = plateau[f"{i}{j}"]
	else:
		if f"{i}{j}" in possibilite:
			deplacer(actif, i, j)
			actif = None
			possibilite = None

	# (A faire) On regarde si la case est vide dans une liste plateau. Si elle est pleine, on appele la pièce correspondante


def deplacer(piece, i, j):
	i0, j0 = piece.i, piece.j
	plateau[f'{piece.i}{piece.j}'] = None #Vide la case d'ou la pièce part
	piece.i = i
	piece.j = j
	plateau[f'{i}{j}'] = piece #Met la pièce à sa nouvelle coodonnée
	actualiser_deux_pieces(i0, j0, piece)


def case_hors_plateau(coord):
	i=int(coord[0])
	j=int(coord[0])
	if i < 0 or i>7 or j<0 or j>7:
		return True
	else:
		return False

"""---------Ces classe servent pour les test, les bonnes classes sont dans le fichier classes.py----------------"""
class Pion:
	def __init__(self, equipe, i, j):
		self.equipe = equipe
		self.i = i
		self.j = j
		self.image = PhotoImage(file=f"image/pion_{self.equipe}.png")

	def cases_possibles(self, plateau): #Pour l'instant, ne gère pas le bord du plateau. (erreur pour j=0 et j=7)
		possibilites = []
		if self.equipe == "blanc":
			if case_hors_plateau(f'{self.i+1}{self.j}') == False:
				if plateau[f'{self.i+1}{self.j}'] == None:
					possibilites.append(f'{self.i+1}{self.j}')
			if case_hors_plateau(f'{self.i+1}{self.j+1}') == False:
				if plateau[f'{self.i+1}{self.j+1}'] != None:
					possibilites.append(f'{self.i+1}{self.j+1}')
			if case_hors_plateau(f'{self.i+1}{self.j-1}') == False:
				if plateau[f'{self.i+1}{self.j-1}'] != None:
					possibilites.append(f'{self.i+1}{self.j-1}')
		if self.equipe == "noir":
			if case_hors_plateau(f'{self.i-1}{self.j}') == False:
				if plateau[f'{self.i-1}{self.j}'] == None:
					possibilites.append(f'{self.i-1}{self.j}')
			if case_hors_plateau(f'{self.i-1}{self.j-1}') == False:
				if plateau[f'{self.i-1}{self.j-1}'] != None:
					possibilites.append(f'{self.i-1}{self.j}')
			if case_hors_plateau(f'{self.i-1}{self.j+1}') == False:
				if plateau[f'{self.i-1}{self.j+1}'] != None:
					possibilites.append(f'{self.i-1}{self.j+1}')

		print(possibilites)

		return possibilites

class Tour:
	def __init__(self, equipe, i, j):
		self.equipe = equipe
		self.i = i
		self.j = j
		self.image = None

class Cavalier:
	def __init__(self, equipe, i, j):
		self.equipe = equipe
		self.i = i
		self.j = j
		self.image = None


class Fou:
	def __init__(self, equipe, i, j):
		self.equipe = equipe
		self.i = i
		self.j = j
		self.image = None

class Roi:
	def __init__(self, equipe, i, j):
		self.equipe = equipe
		self.i = i
		self.j = j
		self.image = PhotoImage(file=f"image/roi_{self.equipe}.png")

class Reine:
	def __init__(self, equipe, i, j):
		self.equipe = equipe
		self.i = i
		self.j = j
		self.image = None

"""---------Ces classe servent pour les test, les bonnes classes sont dans le fichier classes.py----------------"""



def placement_pieces(): #Sert à placer les pieces sur le plateau (sans les affichées)
	global plateau
	for i in range(8): #Placement des pions
		pion = Pion("blanc", 1, i)
		plateau[f'{1}{i}'] = pion

		pion = Pion("noir", 6, i)
		plateau[f'{6}{i}'] = pion

	#Placement des tours
	for i in range(2):
		plateau[f'{0}{i*7}'] = Tour("blanc", 0, i*7)
		plateau[f'{7}{i*7}'] = Tour("noir", 7, i*7)

		#Placement des cavaliers
		plateau[f'{0}{1+i*5}'] = Cavalier("blanc", 0, 1+i*5)
		plateau[f'{7}{1+i*5}'] = Cavalier("noir", 7, 1+i*5)

		#Placement des fous
		plateau[f'{0}{2+i*3}'] = Fou("blanc", 0, 2+i*4)
		plateau[f'{7}{2+i*3}'] = Fou("noir", 7, 2+i*4)

	#reines et rois
	plateau[f'{0}{4}'] = Roi("blanc", 0, 4)
	plateau[f'{7}{3}'] = Roi("noir", 7, 3)
	plateau[f'{0}{3}'] = Reine("blanc", 0, 3)
	plateau[f'{7}{4}'] = Reine("noir", 7, 4)


fen = Tk()
fen.title("jeu d'échec")
fen.resizable(False, False) #Empêche de redimentionner la fenêtre.

possibilite = None #servira à stoquer les cases possibles des pièces en mouvement
actif = None #stoque la pièce en cours de déplacement
buttons_cases, plateau = creation_terrain() #création du plateau.

placement_pieces() #mise en place des pièces (sans affichage)

actualiser() #Affiche les pièces
p_test = plateau["11"].cases_possibles(plateau)
print(p_test)
fen.mainloop()
