from tkinter import *
from time import *
from os import path

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

	def couleur_cases(self): #Définit si une case est noire ou blanche selon sa position
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
			size = 10
			self.image_possibilite = self.canvas.create_oval(self.canvas.winfo_reqwidth()//2-size, self.canvas.winfo_reqheight()//2-size, self.canvas.winfo_reqwidth()//2+size, self.canvas.winfo_reqheight()//2+size, fill="#857c1b")


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

		if fen.partie["actif"] == 42: #Cette partie est désactivée car elle ne fonctionne pas actuellement
			i, j = fen.partie["actif"].i, fen.partie["actif"].j
			for p in fen.partie["possibilites"]:
				plateau = fen.partie["plateau"].copy()
				plateau[p] = plateau[tuple_to_string((i, j))]
				plateau[tuple_to_string((i, j))] = None
				if est_echec(plateau) != None:
					print("echec !")
		afficher_possibilites(fen)

"""Fonctions de parties"""
def nouvelle_partie(fen, type):
	fen.partie = {}
	fen.partie["type"] = type
	fen.partie["plateau"] = creer_plateau()
	fen.partie["actif"] = None
	fen.partie["possibilites"] = []
	fen.partie["joueur"] = "blanc"
	fen.partie["tour"] = 1
	fen.partie["debut"] = time()
	afficher_partie(fen)

def charger_partie(fen, fichier):
	fen.partie = {}
	if fichier != "":
		fen.partie["plateau"] = {}
		with open(fichier, "r") as fichier:
			lignes = fichier.readlines()
			for i in range(8):
				cases = lignes[i].split()
				for j in range(8):
					if cases[j] == "N":
						piece = None
					elif cases[j] == "P":
						piece = Pion(cases[j+8], i, j, str_to_bool(cases[j+16]))
					elif cases[j] == "T":
						piece = Tour(cases[j+8], i, j, str_to_bool(cases[j+16]))
					elif cases[j] == "C":
						piece = Cavalier(cases[j+8], i, j, str_to_bool(cases[j+16]))
					elif cases[j] == "F":
						piece = Fou(cases[j+8], i, j, str_to_bool(cases[j+16]))
					elif cases[j] == "D":
						piece = Dame(cases[j+8], i, j, str_to_bool(cases[j+16]))
					elif cases[j] == "R":
						piece = Roi(cases[j+8], i, j, str_to_bool(cases[j+16]))
					fen.partie["plateau"][tuple_to_string((i, j))] = piece
			fen.partie["type"] = lignes[8]
			fen.partie["actif"] = None
			l = 0
			for e in lignes: #Supprime les lignes vides qui apparaissent parfois
				if e == "\n":
					l+=1
			fen.partie["joueur"] = lignes[9+l].replace("\n", "")
			fen.partie["tour"] = int(lignes[10+l])
			fen.partie["debut"] = time()-float(lignes[11+l])
			fen.partie["possibilites"] = []
			afficher_partie(fen)

def sauvegarder_partie(nom, partie):
	with open("parties/" + nom + ".save", "w") as fichier:
		for i in range(8):
			ligne_1 = ""
			ligne_2 = ""
			ligne_3 = ""
			for j in range(8):
				if partie["plateau"][tuple_to_string((i, j))] == None:
					ligne_1 += "N "
					ligne_2 += "N "
					ligne_3 += "N "
				else:
					ligne_1 += partie["plateau"][tuple_to_string((i, j))].lettre + " "
					ligne_2 += partie["plateau"][tuple_to_string((i, j))].equipe + " "
					ligne_3 += str(partie["plateau"][tuple_to_string((i, j))].deplace) + " "
			ligne = ligne_1+ligne_2+ligne_3
			ligne += "\n"
			fichier.write(ligne)
		fichier.write(partie["type"] + "\n")
		fichier.write(partie["joueur"] + "\n")
		fichier.write(str(partie["tour"]) + "\n")
		fichier.write(str(time()-partie["debut"]))

def quitter_partie(fen):
	fen.canvas.delete("all")
	fen.afficher_accueil()

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

def str_to_bool(a):
	if a == "True":
		return True
	return False

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
	#print(est_echec(fen.partie["plateau"]))

def passer_tour(fen):
	if fen.partie["joueur"] == "blanc":
		fen.partie["joueur"] = "noir"
	else:
		fen.partie["joueur"] = "blanc"
		fen.partie["tour"] += 1
	actualiser_affichage(fen )


"""Fonctions d'affichage"""
def afficher_partie(fen):
	afficher_plateau(fen, fen.partie["plateau"])
	afficher_infos(fen)
	fen.bouton_fermer["command"] = lambda: afficher_input_sauvegarde(fen, True)

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

def afficher_infos(fen):
	fen.affichage["bouton_menu"] = Button(fen, text="Quitter", bg=fen.bouton_bg, fg=fen.bouton_fg, activebackground=fen.bouton_activebg, activeforeground=fen.bouton_activefg, font="Helvetica 14", command=lambda: afficher_input_sauvegarde(fen), border=0, relief=SUNKEN)
	fen.affichage["bouton_menu"].bind("<Enter>", fen.entree_bouton)
	fen.affichage["bouton_menu"].bind("<Leave>", fen.sortie_bouton)
	fen.affichage_id["bouton_menu"] = fen.canvas.create_window(fen.canvas.winfo_width() - 50, fen.canvas.winfo_height() - 50, window=fen.affichage["bouton_menu"], anchor=CENTER)
	fen.affichage_id["text_joueur"] = fen.canvas.create_text(10, 20, text="Tour du joueur " + fen.partie["joueur"], fill=fen.bouton_fg, font="Helvetica 16", anchor=NW)
	fen.affichage_id["text_tour"] = fen.canvas.create_text(10, 60, text="Tour n°" + str(fen.partie["tour"]), fill=fen.bouton_fg, font="Helvetica 16", anchor=NW)


def actualiser_affichage(fen):
	fen.canvas.itemconfig(fen.affichage_id["text_joueur"], text="Tour du joueur " + fen.partie["joueur"])
	fen.canvas.itemconfig(fen.affichage_id["text_tour"], text="Tour n°" + str(fen.partie["tour"]))

class Popup_sauvegarde(Canvas):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		fen = self._root()
		self.fermer = False #Définit si l'app doit se fermer lors de sa validation
		self.entree_var = StringVar()
		self.entree_var.trace_add("write", self.actualiser)

		self.entree = Entry(self, textvariable=self.entree_var, font="Helvetica 16", width=30, justify=CENTER)
		self.entree.focus_set()
		self.bouton_valider = Button(self, text="Valider", command=self.valider, bg=fen.bouton_bg, fg=fen.bouton_fg, activebackground=fen.bouton_activebg, activeforeground=fen.bouton_activefg, font="Helvetica 16", border=0, relief=SUNKEN)
		self.bouton_annuler = Button(self, text="Annuler", command=self.destroy, bg=fen.bouton_bg, fg=fen.bouton_fg, activebackground=fen.bouton_activebg, activeforeground=fen.bouton_activefg, font="Helvetica 16", border=0, relief=SUNKEN)

		self.bouton_valider.bind("<Enter>", fen.entree_bouton)
		self.bouton_valider.bind("<Leave>", fen.sortie_bouton)
		self.bouton_annuler.bind("<Enter>", fen.entree_bouton)
		self.bouton_annuler.bind("<Leave>", fen.sortie_bouton)

		self.create_text(self.winfo_reqwidth()//2, self.winfo_reqheight()//6, text="Entrez le nom de la partie:", font="Helvetica 18", fill=fen.bouton_fg)
		self.create_window(self.winfo_reqwidth()//2, self.winfo_reqheight()//3, window=self.entree)
		self.info = self.create_text(self.winfo_reqwidth()//2, self.winfo_reqheight()//2, text="Attention: vous allez quitter sans sauvegarder !", font="Helvetica 16", fill=fen.bouton_fg)
		self.create_window(self.winfo_reqwidth()//2-self.winfo_reqwidth()//6, self.winfo_reqheight()//1.25, window=self.bouton_valider)
		self.create_window(self.winfo_reqwidth()//2+self.winfo_reqwidth()//6, self.winfo_reqheight()//1.25, window=self.bouton_annuler)

	def valider(self):
		nom = self.entree_var.get()
		validation = self.est_valide(nom)
		if validation == "Nom valide." or validation == "Attention: vous allez écraser une sauvegarde !":
			sauvegarder_partie(nom, self._root().partie)
			quitter_partie(self._root())
			if self.fermer:
				self._root().little.quit()
		elif validation == "Attention: vous allez quitter sans sauvegarder !":
			quitter_partie(self._root())
			if self.fermer:
				self._root().little.quit()

	def actualiser(self, a, b, c):
		fichier = self.entree_var.get()
		self.itemconfig(self.info, text=self.est_valide(fichier))

	def est_valide(self, fichier):
		message = ""
		if fichier == "":
			message = "Attention: vous allez quitter sans sauvegarder !"
		else:
			for char in ["\\", "/", ":", "*", "?", '"', "<", ">"]:
				if char in fichier:
					message = "Nom invalide !"
			if message != "Nom invalide !":
				if path.exists("parties/" + fichier + ".save"):
					message = "Attention: vous allez écraser une sauvegarde !"
				else:
					message = "Nom valide."
		return message

	def afficher(self, fermer):
		self.fermer = fermer
		if self._root().affichage_id["popup"] != None:
			self._root().canvas.delete(self._root().affichage_id["popup"])
		self._root().affichage_id["popup"] = self._root().canvas.create_window(self._root().winfo_width()//2, self._root().winfo_height()//2, window=self)


def afficher_input_sauvegarde(fen, fermer=False): #Sert à afficher la fenêtre de demande de sauvegarde
	Popup_sauvegarde(fen, width=fen.winfo_width()//1.25, height=fen.winfo_height()//2, bg="#3d3937", border=0, highlightthickness=0).afficher(fermer)


"""Fonctions d'échec et mat"""
def est_echec(plateau):
	for case in plateau:
		if plateau[case] != None:
			for p in plateau[case].cases_possibles(plateau):
				if type(plateau[p]) == classes.Roi:
					return plateau[p].equipe
	return None
