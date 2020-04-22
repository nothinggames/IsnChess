from tkinter import *
from time import *
from os import path
import json

import classes
from classes import *

class Case():
	def __init__(self, fen, i, j):
		self.fen = fen
		self.i, self.j = i, j
		self.image_piece = None
		self.image_possibilite1 = None
		self.image_possibilite2 = None
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
		if self.image_possibilite1 != None:
			self.canvas.delete(self.image_possibilite1)
			self.canvas.delete(self.image_possibilite2)
			self.image_possibilite2 = None
		if p == True:
			size = 12
			self.image_possibilite1 = self.canvas.create_oval(self.canvas.winfo_reqwidth()//2-size, self.canvas.winfo_reqheight()//2-size, self.canvas.winfo_reqwidth()//2+size, self.canvas.winfo_reqheight()//2+size,
				fill="#545450", width=0)
			size = 7
			self.image_possibilite2 = self.canvas.create_oval(self.canvas.winfo_reqwidth()//2-size, self.canvas.winfo_reqheight()//2-size, self.canvas.winfo_reqwidth()//2+size, self.canvas.winfo_reqheight()//2+size,
				fill="#2e2e2b", width=0)


	def click(self, e):
		fen = self.fen
		i, j = self.i, self.j
		if fen.partie["terminee"] == False:
			if fen.partie["possibilites"] == []:
				if fen.partie["plateau"][tuple_to_string((i, j))] != None and fen.partie["plateau"][tuple_to_string((i, j))].equipe == fen.partie["joueur"]:
					fen.partie["actif"] = fen.partie["plateau"][tuple_to_string((i, j))]
					fen.partie["possibilites"] = fen.partie["plateau"][tuple_to_string((i, j))].cases_possibles(fen.partie["plateau"])
					fen.partie["possibilites"] = attention_messir(fen, fen.partie["possibilites"], fen.partie["actif"])
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
						fen.partie["possibilites"] = attention_messir(fen, fen.partie["possibilites"], fen.partie["actif"])
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
	fen.partie["tour"] = 1
	fen.partie["debut"] = time()
	if type == "blitz":
		fen.partie["temps_passe"] = time() + 61 #nb secondes
	fen.partie["temps_enregistre"] = 0
	fen.partie["pieces_mangees_blanc"] = []
	fen.partie["pieces_mangees_noir"] = []
	fen.partie["positions_rois"] = {"blanc":"04", "noir":"73"}
	fen.partie["terminee"] = False
	afficher_partie(fen)

def sauvegarder_partie(nom, partie):
	with open("parties/" + nom + ".json", "w") as fichier:
		donnees = {
			"type": partie["type"],
			"joueur": partie["joueur"],
			"tour": partie["tour"],
			"temps_enregistre": time()-partie["debut"]+partie["temps_enregistre"],
			"pieces_mangees_blanc": partie[f"pieces_mangees_blanc"],
			"pieces_mangees_noir": partie[f"pieces_mangees_noir"],
			"plateau": plateau_to_lettres(partie["plateau"])
		}
		if partie["type"] == "blitz":
			donnees["temps_restant"] = partie["temps_passe"] - time()
		json.dump(donnees, fichier, indent=4)

def charger_partie(fen, fichier):
	fen.partie = {}
	if fichier != "":
		fen.partie["plateau"] = {}
		with open(fichier, "r") as fichier:
			donnees = json.load(fichier)
			fen.partie = {
				"type": donnees["type"],
				"joueur": donnees["joueur"],
				"tour": donnees["tour"],
				"debut": time(),
				"temps_enregistre": donnees["temps_enregistre"],
				"pieces_mangees_blanc": donnees["pieces_mangees_blanc"],
				"pieces_mangees_noir": donnees["pieces_mangees_noir"],
				"plateau": lettres_to_plateau(donnees["plateau"]),
				"actif": None,
				"possibilites": [],
				"positions_rois" : {}
			}
			for e in fen.partie["plateau"]:
				if type(fen.partie["plateau"][e]) == classes.Roi:
					if fen.partie["plateau"][e].equipe == "noir":
						fen.partie["positions_rois"]["noir"] = e
					else:
						fen.partie["positions_rois"]["blanc"] = e
			if len(fen.partie["positions_rois"]) == 2:
				fen.partie["terminee"] = False
			else:
				fen.partie["terminee"] = True
			if donnees["type"] == "blitz":
				fen.partie["temps_passe"] = time() + donnees["temps_restant"]
			afficher_partie(fen)

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

def plateau_to_lettres(plateau):
	final = {}
	equipe = {"blanc": "B", "noir": "N"}
	deplace = {"True": "T", "False": "F"}
	for i in range(8):
		for j in range(8):
			if plateau[tuple_to_string((i, j))] != None:
				final[tuple_to_string((i, j))] = plateau[tuple_to_string((i, j))].lettre + equipe[plateau[tuple_to_string((i, j))].equipe] + deplace[str(plateau[tuple_to_string((i, j))].deplace)]
			else:
				final[tuple_to_string((i, j))] = "NNN"
	return final

def lettres_to_plateau(lettres):
	plateau = {}
	equipe = {"B": "blanc", "N": "noir"}
	deplace = {"T": True, "F": False}
	for i in range(8):
		for j in range(8):
			case = lettres[tuple_to_string((i, j))]
			if case[0] == "N":
				piece = None
			elif case[0] == "P":
				piece = Pion(equipe[case[1]], i, j, deplace[case[2]])
			elif case[0] == "T":
				piece = Tour(equipe[case[1]], i, j, deplace[case[2]])
			elif case[0] == "C":
				piece = Cavalier(equipe[case[1]], i, j, deplace[case[2]])
			elif case[0] == "F":
				piece = Fou(equipe[case[1]], i, j, deplace[case[2]])
			elif case[0] == "D":
				piece = Dame(equipe[case[1]], i, j, deplace[case[2]])
			elif case[0] == "R":
				piece = Roi(equipe[case[1]], i, j, deplace[case[2]])
			plateau[tuple_to_string((i, j))] = piece
	return plateau

"""Fonctions de jeu"""
def deplacer(fen, piece, i, j):
	i0, j0 = piece.i, piece.j
	fen.partie["plateau"][tuple_to_string((i0, j0))] = None
	if type(piece) == classes.Pion: #Promotion
		if i == 0 or i == 7:
			piece = classes.Dame(piece.equipe, i, j)
	if type(piece) == classes.Roi:
		fen.partie["positions_rois"][fen.partie["joueur"]] = f"{i}{j}"
	if fen.partie["plateau"][tuple_to_string((i, j))] != None:
		fen.partie[f"pieces_mangees_{fen.partie['plateau'][tuple_to_string((i, j))].equipe}"].append(fen.partie["plateau"][tuple_to_string((i, j))].lettre)
		fen.affichage["canvas_mangees"].ajouter_image(fen.partie["plateau"][tuple_to_string((i, j))].equipe, fen.partie["plateau"][tuple_to_string((i, j))].image_name)
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
		fen.partie["tour"] += 1
	if fen.partie["type"] == "blitz":
		fen.partie["temps_passe"] = time() + 60
	actualiser_affichage(fen)
	echec = est_echec(fen, fen.partie["plateau"]) #Vérifie si le roi du joueur qui va joueur est en échec
	if echec:
		mat = est_mat(fen)#On verifie maintenant le mat
		if mat:
			fen.partie["terminee"] = True
			fen.boutons_cases[tuple_to_string(fen.partie["positions_rois"][fen.partie['joueur']])].canvas["bg"] = "red"
			PopupInfo(fen, width=fen.winfo_width()//1.25, height=fen.winfo_height()//3, bg="#3d3937", border=0, highlightthickness=0).afficher(f"Le joueur {fen.partie['joueur']} a perdu !")
		else:
			PopupInfo(fen, width=fen.winfo_width()//1.25, height=fen.winfo_height()//3, bg="#3d3937", border=0, highlightthickness=0).afficher(f"Le Roi {fen.partie['joueur']} est en échec !")


"""Fonctions d'affichage"""
class PieceMangees():
	def __init__(self, fen, width, height):
		self.fen = fen
		self.canvas = Canvas(fen, width=width, height=height, border=0, highlightthickness=0, bg="#262626")
		self.pieces = {"blanc": [], "noir": []}
		self.coords = {"blanc": 0, "noir": self.canvas.winfo_reqwidth()//2}

	def ajouter_image(self, equipe, image):
		self.pieces[equipe].append(obtenir_image(image, self.canvas.winfo_reqwidth()//2, self.canvas.winfo_reqheight()//15, equipe))
		self.canvas.create_image(self.coords[equipe], (len(self.pieces[equipe]))*self.canvas.winfo_height()//15, anchor=SW, image=self.pieces[equipe][len(self.pieces[equipe])-1])


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
	fen.affichage["bouton_matchnul"] = Button(fen, text="Match Nul", bg=fen.bouton_bg, fg=fen.bouton_fg, activebackground=fen.bouton_activebg, activeforeground=fen.bouton_activefg, font="Helvetica 14", command=lambda: afficher_input_sauvegarde(fen), border=0, relief=SUNKEN)
	fen.affichage["bouton_matchnul"].bind("<Enter>", fen.entree_bouton)
	fen.affichage["bouton_matchnul"].bind("<Leave>", fen.sortie_bouton)
	fen.affichage_id["bouton_menu"] = fen.canvas.create_window(fen.canvas.winfo_width() - 50, fen.canvas.winfo_height() - 22, window=fen.affichage["bouton_menu"], anchor=CENTER)
	fen.affichage_id["bouton_matchnul"] = fen.canvas.create_window(fen.canvas.winfo_width() - 50, fen.canvas.winfo_height() - 66, window=fen.affichage["bouton_matchnul"], anchor=CENTER)
	fen.affichage_id["text_joueur"] = fen.canvas.create_text(10, 20, text="☺ Tour du joueur " + fen.partie["joueur"], fill=fen.bouton_fg, font="Helvetica 16", anchor=NW)
	fen.affichage_id["text_tour"] = fen.canvas.create_text(10, 60, text="↔ Tour n°" + str(fen.partie["tour"]), fill=fen.bouton_fg, font="Helvetica 16", anchor=NW)

	fen.affichage_id["text_temps_ecoule"] = fen.canvas.create_text(fen.winfo_width()//2.5, 20, text="⏲ Temps écoulé: 00:00:00", fill=fen.bouton_fg, font="Helvetica 16", anchor=NW)
	if fen.partie["type"] == "blitz":
		fen.affichage_id["text_temps_restant"] = fen.canvas.create_text(fen.winfo_width()//2.5, 60, text=strftime("{} Temps restant: %H:%M:%S", gmtime(
		fen.partie["temps_passe"] - time())).replace("{}", "⏲"), fill=fen.bouton_fg, font="Helvetica 16", anchor=NW)
	else:
		fen.affichage_id["text_temps_restant"] = fen.canvas.create_text(fen.winfo_width()//2.5, 60, text="⏲ Temps restant: ∞", fill=fen.bouton_fg, font="Helvetica 16", anchor=NW)
	fen.after(1000, lambda: actualiser_horloges(fen))

	fen.affichage["canvas_mangees"] = PieceMangees(fen, 100-2*100//8, fen.canvas.winfo_height()//1.22)
	fen.affichage_id["canvas_mangees"] = fen.canvas.create_window(fen.canvas.winfo_width() - 100+100//8, 20, window=fen.affichage["canvas_mangees"].canvas, anchor=NW)
	fen.after(10, lambda: afficher_mangees(fen)) #Il est necessair d'attendre un peu pour que la fenêtre s'initialise correctement

def afficher_mangees(fen):
	for piece in fen.partie["pieces_mangees_blanc"]:
		fen.affichage["canvas_mangees"].ajouter_image("blanc", IMAGES[piece.replace("\n", "") + "_blanc"])
	for piece in fen.partie["pieces_mangees_noir"]:
		fen.affichage["canvas_mangees"].ajouter_image("noir", IMAGES[piece.replace("\n", "") + "_noir"])

def actualiser_affichage(fen):
	fen.canvas.itemconfig(fen.affichage_id["text_joueur"], text="☺ Tour du joueur " + fen.partie["joueur"])
	fen.canvas.itemconfig(fen.affichage_id["text_tour"], text="↔ Tour n°" + str(fen.partie["tour"]))

def actualiser_horloges(fen):
	if fen.partie["type"] == "menu":
		return
	if fen.partie["terminee"] == True:
		return
	fen.canvas.itemconfig(fen.affichage_id["text_temps_ecoule"], text=strftime("{} Temps écoulé: %H:%M:%S", gmtime(time()-fen.partie["debut"]+fen.partie["temps_enregistre"])).replace("{}", "⏲"))
	if fen.partie["type"] == "blitz":
		if fen.partie["temps_passe"] - time() <= 0:
			passer_tour(fen)
		if fen.partie["temps_passe"] - time() <= 31:
			color = "#b81106"
		else:
			color = fen.bouton_fg
		fen.canvas.itemconfig(fen.affichage_id["text_temps_restant"], text=strftime("{} Temps restant: %H:%M:%S", gmtime(
			fen.partie["temps_passe"] - time())).replace("{}", "⏲"), fill=color)

	fen.after(1000, lambda: actualiser_horloges(fen))

class PopupInfo(Canvas):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		fen = self._root()
		self.text = self.create_text(self.winfo_reqwidth()//2, self.winfo_reqheight()//3, justify=CENTER, font="Helvetica 18", fill=fen.bouton_fg)
		self.bouton_valider = Button(self, text="Valider", command=self.destroy, bg=fen.bouton_bg, fg=fen.bouton_fg, activebackground=fen.bouton_activebg, activeforeground=fen.bouton_activefg, font="Helvetica 16", border=0, relief=SUNKEN)
		self.bouton_valider.bind("<Enter>", fen.entree_bouton)
		self.bouton_valider.bind("<Leave>", fen.sortie_bouton)
		self.create_window(self.winfo_reqwidth()//2, self.winfo_reqheight()//1.25, window=self.bouton_valider)
	def afficher(self, message, action=None):
		if action != None:
			self.bouton_valider["command"] = action
		self.itemconfig(self.text, text=message)
		if self._root().affichage_id["popup"] != None:
			self._root().canvas.delete(self._root().affichage_id["popup"])
		self._root().affichage_id["popup"] = self._root().canvas.create_window(self._root().winfo_width()//2, self._root().winfo_height()//2, window=self)



class PopupSauvegarde(Canvas):
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
				if path.exists("parties/" + fichier + ".json"):
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
	PopupSauvegarde(fen, width=fen.winfo_width()//1.25, height=fen.winfo_height()//2, bg="#3d3937", border=0, highlightthickness=0).afficher(fermer)


"""Fonctions d'échec, mat et roi non déplaçable"""
def est_echec(fen, plateau):
	roi = plateau[fen.partie["positions_rois"][fen.partie["joueur"]]]
	possibilites, menaces = roi.possibilite_menace(plateau, [f"{roi.i}{roi.j}"])
	if possibilites == []:
		return True
	else:
		return False

def est_mat(fen):
	plateau = fen.partie["plateau"]
	roi = plateau[fen.partie["positions_rois"][fen.partie["joueur"]]]
	if roi.cases_possibles(plateau) == [] and mouvement_toutes_pieces(fen):
		return True
	else:
		return False

def attention_messir(fen, possibilites, piece):
	possibilite_finales = possibilites.copy()
	if type(piece) != classes.Roi:
		for e in possibilites:
			plateau_fictif = fen.partie["plateau"].copy()
			plateau_fictif[e] = piece
			plateau_fictif[f"{piece.i}{piece.j}"] = None
			if est_echec(fen, plateau_fictif):
				possibilite_finales.remove(e)
	return possibilite_finales


def mouvement_toutes_pieces(fen): #Consomme beaucoup de puissance, on calcul toutes les possibilitées de toutes les pieces alliés afin de savoir si elles peuvent défendre le roi
	if fen.partie["joueur"] == "noir":
		joueur = "blanc"
	else:
		joueur = "noir"
	plateau = fen.partie["plateau"]
	for e in plateau:
		if plateau[e] != None and plateau[e].equipe != fen.partie["actif"].equipe:
			possibilites = plateau[e].cases_possibles(plateau)
			possibilites = attention_messir(fen, possibilites, plateau[e])
			if possibilites != []:
				return False
	return True