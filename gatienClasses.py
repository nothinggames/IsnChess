from tkinter import *
from fonctions import *

"""Tout ce qui commence par gatien est en cours de modif, ce n'est pas une vertion finale. Ne le modifiez pas (sinon le git bug)"""

# Pion terminé à 95%, il manque la promotion
class Pion():
	def __init__(self, equipe, i, j):
		self.equipe = equipe
		self.i = i
		self.j = j
		self.deplace = False
		self.image = obtenir_image(f"image/pion_{self.equipe}.png")
		self.lettre = "P"

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
	def __init__(self, equipe, i, j):
		self.equipe = equipe
		self.i = i
		self.j = j
		self.deplace = False
		self.image = obtenir_image(f"image/tour_{self.equipe}.png")
		self.lettre = "T"

	def cases_possibles(self, plateau):
		possibilites = []
		possibilites += obtenir_possibilites(plateau, self.i, self.j, 1, 0)
		possibilites += obtenir_possibilites(plateau, self.i, self.j, -1, 0)
		possibilites += obtenir_possibilites(plateau, self.i, self.j, 0, 1)
		possibilites += obtenir_possibilites(plateau, self.i, self.j, 0, -1)
		return possibilites


class Fou():
	def __init__(self, equipe, i, j):
		self.equipe = equipe
		self.i = i
		self.j = j
		self.deplace = False
		self.image = obtenir_image(f"image/fou_{self.equipe}.png")
		self.lettre = "F"

	def cases_possibles(self, plateau):
		possibilites = []
		possibilites += obtenir_possibilites(plateau, self.i, self.j, 1, 1)
		possibilites += obtenir_possibilites(plateau, self.i, self.j, -1, -1)
		possibilites += obtenir_possibilites(plateau, self.i, self.j, 1, -1)
		possibilites += obtenir_possibilites(plateau, self.i, self.j, -1, 1)
		return possibilites


class Dame():
	def __init__(self, equipe, i, j):
		self.equipe = equipe
		self.i = i
		self.j = j
		self.deplace = False
		self.image = obtenir_image(f"image/dame_{self.equipe}.png")
		self.lettre = "D"

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
	def __init__(self, equipe, i, j):
		self.equipe = equipe
		self.i = i
		self.j = j
		self.deplace = False
		self.image = obtenir_image(f"image/roi_{self.equipe}.png")
		self.lettre = "R"

	def cases_possibles(self, plateau):
		possibilites = []
		for i in range(-1, 2):
			for j in range(-1, 2):
				if (i, j) != (0, 0):
					case = (self.i + i, self.j + j)
					if not case_hors_plateau(case):
						if plateau[tuple_to_string(case)] == None or plateau[
							tuple_to_string(case)].equipe != self.equipe:
							if self.echec(i, j, plateau):
								possibilites.append(tuple_to_string(case))
		print(possibilites)
		return possibilites

	def echec(self, i, j, plateau):#recoit une case à vérifier. Si la case est dangereuse, return False si on peut y aller, return True
		#On va créer une dame et un cavalier fictif sur cette case. On teste leurs mouvement, si le cavalier recontre un
		#cavalier enemis, return false. Si la dame recontre quelque chose, on verifie les possibilitées de mouvement de cette
		#chose. Si cela atteint la case, return False, sinon return True.
		print("OK 1")
		cavalier = Cavalier(self.equipe, i, j)
		cases_a_tester = cavalier.cases_possibles(plateau)
		for e in cases_a_tester:
			if plateau[e] != None and plateau[e].lettre == "C":
				print("attention messir")
				return False
		return True

class Cavalier():
	def __init__(self, equipe, i, j):
		self.equipe = equipe
		self.i = i
		self.j = j
		self.deplace = False
		self.image = obtenir_image(f"image/cavalier_{self.equipe}.png")
		self.lettre = "C"

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


def obtenir_possibilites(plateau, i, j, a, b):
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
			if plateau[tuple_to_string(case)].equipe != plateau[f"{i}{j}"].equipe:
				possibilites.append(tuple_to_string(case))
			return possibilites

