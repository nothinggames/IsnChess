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

#Pion terminé à 95%, il manque la promotion
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
			(self.i + 1*k, self.j),
			(self.i + 1*k, self.j - 1),
			(self.i + 1*k, self.j + 1)
		]
		final = []
		if not self.deplace:
			possibilites.append((self.i + 2*k, self.j))
		i = 0
		for e in possibilites:
			if not case_hors_plateau(e):
				if i == 0 or i==3:
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
		possibilites += obtenir_possibilites(plateau, self.i, self.j, 1, 0)
		possibilites += obtenir_possibilites(plateau, self.i, self.j, -1, 0)
		possibilites += obtenir_possibilites(plateau, self.i, self.j, 0, 1)
		possibilites += obtenir_possibilites(plateau, self.i, self.j, 0, -1)
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
		possibilites += obtenir_possibilites(plateau, self.i, self.j, 1, 1)
		possibilites += obtenir_possibilites(plateau, self.i, self.j, -1, -1)
		possibilites += obtenir_possibilites(plateau, self.i, self.j, 1, -1)
		possibilites += obtenir_possibilites(plateau, self.i, self.j, -1, 1)
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
		possibilites += obtenir_possibilites(plateau, self.i, self.j, 0, -1)
		possibilites += obtenir_possibilites(plateau, self.i, self.j, 0, 1)
		possibilites += obtenir_possibilites(plateau, self.i, self.j, -1, 0)
		possibilites += obtenir_possibilites(plateau, self.i, self.j, 1, 0)
		possibilites += obtenir_possibilites(plateau, self.i, self.j, 1, 1)
		possibilites += obtenir_possibilites(plateau, self.i, self.j, -1, -1)
		possibilites += obtenir_possibilites(plateau, self.i, self.j, 1, -1)
		possibilites += obtenir_possibilites(plateau, self.i, self.j, -1, 1)
		return possibilites
		possibilites = []
		possibilites += obtenir_possibilites(plateau, self.i, self.j, 1, 0)
		possibilites += obtenir_possibilites(plateau, self.i, self.j, -1, 0)


class Roi():
	def __init__(self, equipe, i, j, deplace=False):
		self.equipe = equipe
		self.i = i
		self.j = j
		self.deplace = deplace
		self.lettre = "R"
		self.image_name = IMAGES[f"{self.lettre}_{self.equipe}"]
		self.image = obtenir_image(self.image_name)

	def cases_possibles(self, plateau):
		possibilites = []
		for i in range(-1, 2):
			for j in range(-1, 2):
				if (i, j) != (0, 0):
					case = (self.i + i, self.j + j)
					if not case_hors_plateau(case):
						if plateau[tuple_to_string(case)] == None or plateau[tuple_to_string(case)].equipe != self.equipe:
							possibilites.append(tuple_to_string(case))
		return possibilites


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
			i*=-1
			for b in range(2):
				j *= -1
				case = (self.i + i, self.j + j)
				if not case_hors_plateau(case):
					if plateau[tuple_to_string(case)] == None or plateau[tuple_to_string(case)].equipe != self.equipe:
						possibilites.append(tuple_to_string(case))
		i = 1
		j = 2
		for a in range(2):
			i*=-1
			for b in range(2):
				j *= -1
				case = (self.i + i, self.j + j)
				if not case_hors_plateau(case):
					if plateau[tuple_to_string(case)] == None or plateau[tuple_to_string(case)].equipe != self.equipe:
						possibilites.append(tuple_to_string(case))
		return possibilites


def obtenir_possibilites(plateau, i, j, a, b):
	n = 0
	m = 0
	possibilites = []
	while True:
		n += 1
		m += 1
		case = (i + n*a, j + m*b)
		if case_hors_plateau(case):
			return possibilites
		if plateau[tuple_to_string(case)] == None:
			possibilites.append(tuple_to_string(case))
		else:
			if plateau[tuple_to_string(case)].equipe != plateau[tuple_to_string((i, j))].equipe:
				possibilites.append(tuple_to_string(case))
			return possibilites

"""Fonctions utilitaires"""
def tuple_to_string(a):
	return f"{a[0]}{a[1]}"

def obtenir_image(chemin, width=50, height=50):
	img = Image.open(chemin)
	img = img.resize((width, height))
	photoImg = ImageTk.PhotoImage(img)
	return photoImg

def case_hors_plateau(coord):
	i=coord[0]
	j=coord[1]
	if i < 0 or i>7 or j<0 or j>7:
		return True
	else:
		return False