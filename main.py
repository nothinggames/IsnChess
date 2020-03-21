from tkinter import *
from classes import *
from fonctions import *
from time import *

class Bouton():#Cette classe sert à créer et stocker chaque bouton avec ses coordonnées (O, i, j). O est situé en bas à gauche de la fenetre
	#CETTE CLASSE RESTE DANS LE MAIN
	def __init__(self, i, j, frame_plateau, text=""):
		self.i = i #i correspond au numéro de la ligne
		self.j = j #j correspond au numéro de la colone
		self.bouton = Button(frame_plateau, background=self.couleur_cases(), command=lambda: appel_bouton(plateau, self.i, self.j),
						width=10, height=5, image="", bd=0,
							 activebackground=self.couleur_cases(), relief=SUNKEN) #Chaque case est un bouton qui appel la fonction appel_bouton(i, j)
		#self.bouton.bind("<Enter>", self.bouton_entree)
		#self.bouton.bind("<Leave>", self.bouton_sortie)
		self.bouton_grid()


	def changer_image(self, img): #Sert à modifier l'image à afficher lors du placement des pièces ou lors d'un déplacement.
		self.bouton["image"] = img #On modifie l'attribut image de notre bouton.
		if img == "":
			self.bouton["width"] = 10
			self.bouton["height"] = 5
		else:
			self.bouton["width"] = 75
			self.bouton["height"] = 80
		
	def bouton_entree(self, e):
		self.bouton["background"] = "red"

	def bouton_sortie(self, e):
		self.bouton["background"] = self.couleur_cases()


	def couleur_cases(self): #Définit si une case est noir ou blanche selon sa position
		if self.i%2 == 0 and self.j%2 == 0:
			return "black"
		elif self.i%2 != 0 and self.j%2 != 0:
			return "black"
		else:
			return "white"

	def bouton_grid(self): #affiche le bouton.
		self.bouton.grid(row=8-self.i, column=self.j)



#------------------------ceci est la partie appelé par les boutton pieces---------------------------

def appel_bouton(plateau, i, j): #Fonction appelé lors d'un clic sur un bouton, les coordonnées (i, j) donnent le bouton activé
	#print(plateau[f'{i}{j}
	global actif, possibilite, joueur
	if possibilite == None:
		if plateau[f'{i}{j}'] != None and plateau[f'{i}{j}'].equipe == joueur:
			possibilite = plateau[f'{i}{j}'].cases_possibles(plateau)
			actif = plateau[f"{i}{j}"]
			actualier_couleurs(buttons_cases, possibilite)
	else:
		if f"{i}{j}" in possibilite:
			deplacer(plateau, buttons_cases, actif, i, j)
			actif = None
			possibilite = None
			if joueur == "blanc":
				joueur = "noir"
			else:
				joueur = "blanc"
		else:
			if plateau[f'{i}{j}'] != None and plateau[f'{i}{j}'].equipe == joueur:
				possibilite = plateau[f'{i}{j}'].cases_possibles(plateau)
				actif = plateau[f"{i}{j}"]
				actualier_couleurs(buttons_cases, possibilite)
			else:
				actif = None
				possibilite = None
				actualier_couleurs(buttons_cases, possibilite)

	# On regarde si la case est vide dans une liste plateau. Si elle est pleine, on appele la pièce correspondante


def placement_pieces(): #Sert à placer les pieces sur le plateau (sans les affichées)
	#NE PAS DEPLACER CETTE FONCTION
	global plateau
	for i in range(8): #Placement des pions
		pion = Pion("blanc", 1, i)
		plateau[f'{1}{i}'] = pion

		pion = Pion("noir", 6, i)
		plateau[f'{6}{i}'] = pion
		#pion = Pion("noir", 6, i)
		#plateau[f'{1}{i}'] = pion
	#return #NE PAS ENLEVER
	#Placement des tours
	for i in range(2):
		plateau[f'{0}{i * 7}'] = Tour("blanc", 0, i * 7)
		plateau[f'{7}{i * 7}'] = Tour("noir", 7, i * 7)

		# Placement des cavaliers
		plateau[f'{0}{1 + i * 5}'] = Cavalier("blanc", 0, 1 + i * 5)
		plateau[f'{7}{1 + i * 5}'] = Cavalier("noir", 7, 1 + i * 5)

		# Placement des fous
		plateau[f'{0}{2 + i * 3}'] = Fou("blanc", 0, 2 + i * 3)
		plateau[f'{7}{2 + i * 3}'] = Fou("noir", 7, 2 + i * 3)

	#reines et rois
	plateau[f'{0}{4}'] = Roi("blanc", 0, 4)
	plateau[f'{7}{3}'] = Roi("noir", 7, 3)
	plateau[f'{0}{3}'] = Dame("blanc", 0, 3)
	plateau[f'{7}{4}'] = Dame("noir", 7, 4)

def creation_terrain(fen): #initialiser le plateau.

	frame_plateau = Frame(fen) #La frame qui contient les boutons
	buttons_cases = {} #Un dictionnaire qui renvoie le bouton correspondant aux coordonnées ["ij"]
	plateau = {} #Le plateau contion les pièces et les vides, il sera mit dans un fichier externe afin de sauvegarder les parties. (Les pièces sont des class)
	#for i in range(8):
	#	buttons_cases[f'{i}0'] = Bouton(i, 0, frame_plateau, text=i) #Création des boutons
	for i in range(8):
		for j in range(8):
			buttons_cases[f'{i}{j}'] = Bouton(i, j, frame_plateau) #Création des boutons
			plateau[f'{i}{j}'] = None #Création d'un plateau vide
	frame_plateau.grid(row=1, column=0)
	return buttons_cases, plateau

#Barre d'informations
def afficher_barre_info(fen):
	barre_info = {}
	barre_info["frame"] = Frame()
	barre_info["joueur"] = Label(barre_info["frame"], text="Joueur Blanc")
	barre_info["joueur"].grid(row=0, column=0)
	barre_info["frame"].grid(row=0, column=0)
	actualiser_barre_info(fen, barre_info, 0)

def actualiser_barre_info(fen, barre_info, i):
	barre_info["joueur"]["text"] = i
	i += 1
	fen.after(1000, lambda: actualiser_barre_info(fen, barre_info, i))



fen = Tk()
fen.title("jeu d'échec")
fen.resizable(False, False) #Empêche de redimentionner la fenêtre.

possibilite = None #servira à stoquer les cases possibles des pièces en mouvement
actif = None #stoque la pièce en cours de déplacement
joueur = "blanc"

afficher_barre_info(fen)
buttons_cases, plateau = creation_terrain(fen) #création du plateau.

placement_pieces() #mise en place des pièces (sans affichage)

actualiser(plateau, buttons_cases) #Affiche les pièces
#p_test = plateau["11"].cases_possibles(plateau)
#print(p_test)
print(time())
sauvegarde_partie("test.save", plateau, joueur)

fen.mainloop()
