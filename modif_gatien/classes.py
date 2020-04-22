from tkinter import *
from PIL import Image
from PIL import ImageTk

IMAGES = {
	"P_blanc": "images/pion_blanc.png",
	"P_noir": "images/pion_noir.png",
	"T_blanc": "images/tour_blanc.png",
	"T_noir": "images/tour_noir.png",
	"F_blanc": "images/fou_blanc.png",
	"F_noir": "images/fou_noir.png",
	"D_blanc": "images/dame_blanc.png",
	"D_noir": "images/dame_noir.png",
	"R_blanc": "images/roi_blanc.png",
	"R_noir": "images/roi_noir.png",
	"C_blanc": "images/cavalier_blanc.png",
	"C_noir": "images/cavalier_noir.png"
}


# Pion terminé à 95%, il manque la promotion
class Pion():
	def __init__(self, equipe, i, j, deplace=False):
		self.equipe = equipe
		self.i = i
		self.j = j
		self.deplace = deplace
		self.lettre = "P"
		self.image_name = IMAGES[f"{self.lettre}_{self.equipe}"]
		self.image = obtenir_image(self.image_name)

	def cases_possibles(self, plateau):
		if self.equipe == "blanc":
			k = 1
		else:
			k = -1
		possibilites = [
			(self.i + 1 * k, self.j),
			(self.i + 1 * k, self.j - 1),
			(self.i + 1 * k, self.j + 1)
		]
		final = []
		if not self.deplace:
			possibilites.append((self.i + 2 * k, self.j))
		i = 0
		for e in possibilites:
			if not case_hors_plateau(e):
				if i == 0 or i == 3:
					if plateau[tuple_to_string(e)] == None:
						if i == 3:
							if plateau[tuple_to_string(possibilites[0])] == None:
								final.append(tuple_to_string(e))
						else:
							final.append(tuple_to_string(e))
				else:
					if plateau[tuple_to_string(e)] != None and plateau[tuple_to_string(e)].equipe != self.equipe:
						final.append(tuple_to_string(e))
			i += 1
		return final


class Tour():
	def __init__(self, equipe, i, j, deplace=False):
		self.equipe = equipe
		self.i = i
		self.j = j
		self.deplace = deplace
		self.lettre = "T"
		self.image_name = IMAGES[f"{self.lettre}_{self.equipe}"]
		self.image = obtenir_image(self.image_name)

	def cases_possibles(self, plateau):
		possibilites = []
		possibilites += obtenir_possibilites(plateau, self.i, self.j, 1, 0, self.equipe)
		possibilites += obtenir_possibilites(plateau, self.i, self.j, -1, 0, self.equipe)
		possibilites += obtenir_possibilites(plateau, self.i, self.j, 0, 1, self.equipe)
		possibilites += obtenir_possibilites(plateau, self.i, self.j, 0, -1, self.equipe)
		return possibilites


class Fou():
	def __init__(self, equipe, i, j, deplace=False):
		self.equipe = equipe
		self.i = i
		self.j = j
		self.deplace = deplace
		self.lettre = "F"
		self.image_name = IMAGES[f"{self.lettre}_{self.equipe}"]
		self.image = obtenir_image(self.image_name)

	def cases_possibles(self, plateau):
		possibilites = []
		possibilites += obtenir_possibilites(plateau, self.i, self.j, 1, 1, self.equipe)
		possibilites += obtenir_possibilites(plateau, self.i, self.j, -1, -1, self.equipe)
		possibilites += obtenir_possibilites(plateau, self.i, self.j, 1, -1, self.equipe)
		possibilites += obtenir_possibilites(plateau, self.i, self.j, -1, 1, self.equipe)
		return possibilites


class Dame():
	def __init__(self, equipe, i, j, deplace=False):
		self.equipe = equipe
		self.i = i
		self.j = j
		self.deplace = deplace
		self.lettre = "D"
		self.image_name = IMAGES[f"{self.lettre}_{self.equipe}"]
		self.image = obtenir_image(self.image_name)

	def cases_possibles(self, plateau):
		possibilites = []
		possibilites += obtenir_possibilites(plateau, self.i, self.j, 0, -1, self.equipe)
		possibilites += obtenir_possibilites(plateau, self.i, self.j, 0, 1, self.equipe)
		possibilites += obtenir_possibilites(plateau, self.i, self.j, -1, 0, self.equipe)
		possibilites += obtenir_possibilites(plateau, self.i, self.j, 1, 0, self.equipe)
		possibilites += obtenir_possibilites(plateau, self.i, self.j, 1, 1, self.equipe)
		possibilites += obtenir_possibilites(plateau, self.i, self.j, -1, -1, self.equipe)
		possibilites += obtenir_possibilites(plateau, self.i, self.j, 1, -1, self.equipe)
		possibilites += obtenir_possibilites(plateau, self.i, self.j, -1, 1, self.equipe)
		return possibilites
		possibilites = []
		possibilites += obtenir_possibilites(plateau, self.i, self.j, 1, 0, self.equipe)
		possibilites += obtenir_possibilites(plateau, self.i, self.j, -1, 0, self.equipe)


class Roi():
	def __init__(self, equipe, i, j, deplace=False):
		self.equipe = equipe
		self.i = i
		self.j = j
		self.deplace = deplace
		self.lettre = "R"
		self.image_name = IMAGES[f"{self.lettre}_{self.equipe}"]
		self.image = obtenir_image(self.image_name)

	def cases_possibles(self, plateau,
						menace=True):  # Le menace sert à dire si le roi qui apelle la fonction est réel ou fictif
		possibilites = []
		plateau[f"{self.i}{self.j}"] = None
		for i in range(-1, 2):
			for j in range(-1, 2):
				if (i, j) != (0, 0):
					case = (self.i + i, self.j + j)
					if not case_hors_plateau(case):
						if plateau[tuple_to_string(case)] == None or plateau[
							tuple_to_string(case)].equipe != self.equipe:
							possibilites.append(tuple_to_string(case))
		if menace:
			possibilites, d = self.possibilite_menace(plateau, possibilites)
		plateau[f"{self.i}{self.j}"] = self
		return possibilites

	def possibilite_menace(self, plateau, possibilite):
		cases_sures = possibilite[:]
		cases_dangereuses = []
		for e in possibilite:  # On verifi chaque case où peut aller le roi pour voir si elle est dangereuse
			if self.verification_cavalier(plateau, e[0], e[1], cases_sures) or \
					self.verification_tour(plateau, e[0], e[1], cases_sures) or \
					self.verification_fou(plateau, e[0], e[1], cases_sures) or \
					self.verification_pion(plateau, e[0], e[1], cases_sures):
				# self.verification_roi(plateau, e[0], e[1], cases_sures): #Ne marche pas encore
				cases_sures.remove(e)
				cases_dangereuses.append(e)
		return cases_sures, cases_dangereuses

	def verification_tour(self, plateau, i, j, cases_a_verifier):
		tour = Tour(self.equipe, int(i), int(j))  # Pareil pour les tours et la moitié du mouvement de la dame
		for case in tour.cases_possibles(plateau):
			if type(plateau[case]) == Tour or type(plateau[case]) == Dame:
				if f"{i}{j}" in cases_a_verifier:
					return True
		return False

	def verification_roi(self, plateau, i, j, cases_a_verifier):
		roi = Roi(self.equipe, int(i), int(j))  # De même pour le roi adverse
		for case in roi.cases_possibles(plateau, False):
			if type(plateau[case]) == Roi:
				if f"{i}{j}" in cases_a_verifier:
					return True
		return False

	def verification_fou(self, plateau, i, j, cases_a_verifier):
		fou = Fou(self.equipe, int(i), int(j))  # On detecte  fou et dame en diagonale
		for case in fou.cases_possibles(plateau):
			if type(plateau[case]) == Fou or type(plateau[case]) == Dame:
				if f"{i}{j}" in cases_a_verifier:
					return True
		return False

	def verification_cavalier(self, plateau, i, j, cases_a_verifier):
		cav = Cavalier(self.equipe, int(i), int(
			j))  # On creer un cavalier fictif qui va verifier si le case où veux aller le roi est menacée
		for case in cav.cases_possibles(plateau):
			if type(plateau[case]) == Cavalier:
				if f"{i}{j}" in cases_a_verifier:
					return True
		return False

	def verification_pion(self, plateau, i, j, cases_a_verifier):
		pion = Pion(self.equipe, int(i), int(j), True)
		for case in pion.cases_possibles(plateau):
			if type(plateau[case]) == Pion:
				if f"{i}{j}" in cases_a_verifier:
					return True
		return False


class Cavalier():
	def __init__(self, equipe, i, j, deplace=False):
		self.equipe = equipe
		self.i = i
		self.j = j
		self.deplace = deplace
		self.lettre = "C"
		self.image_name = IMAGES[f"{self.lettre}_{self.equipe}"]
		self.image = obtenir_image(self.image_name)

	def cases_possibles(self, plateau):
		possibilites = []
		i = 2
		j = 1
		for a in range(2):
			i *= -1
			for b in range(2):
				j *= -1
				case = (self.i + i, self.j + j)
				if not case_hors_plateau(case):
					if plateau[tuple_to_string(case)] == None or plateau[tuple_to_string(case)].equipe != self.equipe:
						possibilites.append(tuple_to_string(case))
		i = 1
		j = 2
		for a in range(2):
			i *= -1
			for b in range(2):
				j *= -1
				case = (self.i + i, self.j + j)
				if not case_hors_plateau(case):
					if plateau[tuple_to_string(case)] == None or plateau[tuple_to_string(case)].equipe != self.equipe:
						possibilites.append(tuple_to_string(case))
		return possibilites


def obtenir_possibilites(plateau, i, j, a, b, equipe):
	n = 0
	m = 0
	possibilites = []
	while True:
		n += 1
		m += 1
		case = (i + n * a, j + m * b)
		if case_hors_plateau(case):
			return possibilites
		if plateau[tuple_to_string(case)] == None:
			possibilites.append(tuple_to_string(case))
		else:
			if plateau[tuple_to_string(case)].equipe != equipe:
				possibilites.append(tuple_to_string(case))
			return possibilites


"""Fonctions utilitaires"""


def tuple_to_string(a):
	return f"{a[0]}{a[1]}"


def obtenir_image(chemin, width=50, height=50, team=None):
	img = Image.open(chemin)
	if team != None:
		if team == "blanc":
			img.putdata(conserver_couleur(img.getdata(), (230, 230, 230), 25))
		else:
			img.putdata(conserver_couleur(img.getdata(), (25, 25, 25), 25))
	img = img.resize((width, height))
	photoImg = ImageTk.PhotoImage(img)
	return photoImg

def conserver_couleur(datas, couleur, seuil):
	newData = []
	for item in datas:
		if item[0] not in range(couleur[0]-seuil, couleur[0]+seuil+1) or item[1] not in range(couleur[1]-seuil, couleur[1]+seuil+1) or item[2] not in range(couleur[2]-seuil, couleur[2]+seuil+1):
			newData.append((255, 255, 255, 0))
		else:
			newData.append(item)
	return newData


def case_hors_plateau(coord):
	i = coord[0]
	j = coord[1]
	if i < 0 or i > 7 or j < 0 or j > 7:
		return True
	else:
		return False

