from tkinter import *
from fonctions import *

class Pion():
	def __init__(self, equipe, i, j):
		self.equipe = equipe
		self.i = i
		self.j = j
		#self.image = PhotoImage(file=f"image/pion_{self.equipe}.png")
		self.image = obtenir_image(f"image/pion_{self.equipe}.png")
		
	def cases_possibles(self, plateau):
		possibilites = []
		if self.equipe == "blanc":
			if plateau[f'{self.i+1}{self.j}'] == None:
				possibilites.append(f'{self.i+1}{self.j}')
			if plateau[f'{self.i+1}{self.j+1}'] != None:
				possibilites.append(f'{self.i+1}{self.j}')
			if plateau[f'{self.i+1}{self.j-1}'] != None:
				possibilites.append(f'{self.i+1}{self.j}')
		if self.equipe == "noir":
			if plateau[f'{self.i-1}{self.j}'] == None:
				possibilites.append(f'{self.i-1}{self.j}')
			if plateau[f'{self.i-1}{self.j-1}'] != None:
				possibilites.append(f'{self.i-1}{self.j}')
			if plateau[f'{self.i-1}{self.j+1}'] != None:
				possibilites.append(f'{self.i-1}{self.j+1}')
		return possibilites

class Tour():
	def __init__(self, equipe, i, j):
		self.equipe = equipe
		self.i = i
		self.j = j
		self.image = None


	def cases_possibles(self, plateau):
		possibilites = []
		a = 1
		while plateau[f'{self.i+a}{self.j}'] == None:
			possibilites.append(f'{self.i+a}{self.j}')
			a += 1
		while plateau[f'{self.i-a}{self.j}'] == None:
			possibilites.append(f'{self.i-a}{self.j}')
			a += 1
		while plateau[f'{self.i}{self.j+a}'] == None:
			possibilites.append(f'{self.i}{self.j+a}')
			a += 1
		while plateau[f'{self.i}{self.j-a}'] == None:
			possibilites.append(f'{self.i}{self.j-a}')
			a += 1
		return possibilites

class Cavalier():
	def __init__(self, equipe, i, j):
		self.equipe = equipe
		self.i = i
		self.j = j
		self.image = None

	
	def cases_possibles(self, plateau):
		possibilites = []
		for a in range(1, 2):
			if plateau[f'{self.i+a}{self.j}'] == None:
				possibilites.append(f'{self.i+a}{self.j}')
			if plateau[f'{self.i}{self.j+a}'] == None:
				possibilites.append(f'{self.i}{self.j+a}')
			if plateau[f'{self.i-a}{self.j}'] == None:
				possibilites.append(f'{self.i+a}{self.j}')
			if plateau[f'{self.i}{self.j-a}'] == None:
				possibilites.append(f'{self.i}{self.j+a}')
		return possibilites

class Fou():
	def __init__(self, equipe, i, j):
		self.equipe = equipe
		self.i = i
		self.j = j
		self.image = None
	
	def cases_possibles(self):
		possibilites = []
		a = 1
		while plateau[f'{self.i+a}{self.j+a}'] == None:
			possibilites.append(f'{self.i+a}{self.j+a}')
			a += 1
		while plateau[f'{self.i-a}{self.j-a}'] == None:
			possibilites.append(f'{self.i-a}{self.j-a}')
			a += 1
		return possibilites


class Dame():
	def __init__(self, equipe, i, j):
		self.equipe = equipe
		self.i = i
		self.j = j
		self.image = None

		def cases_possibles(self, plateau):
			possibilites = []
			a = 1
			while plateau[f'{self.i+a}{self.j}'] == None:
				possibilites.append(f'{self.i+a}{self.j}')
				a += 1
			while plateau[f'{self.i-a}{self.j}'] == None:
				possibilites.append(f'{self.i-a}{self.j}')
				a += 1
			while plateau[f'{self.i}{self.j+a}'] == None:
				possibilites.append(f'{self.i}{self.j+a}')
				a += 1
			while plateau[f'{self.i}{self.j-a}'] == None:
				possibilites.append(f'{self.i}{self.j-a}')
				a += 1
			while plateau[f'{self.i+a}{self.j+a}'] == None:
				possibilites.append(f'{self.i+a}{self.j+a}')
				a += 1
			while plateau[f'{self.i-a}{self.j-a}'] == None:
				possibilites.append(f'{self.i-a}{self.j-a}')
				a += 1
			return possibilites

class Roi():
	def __init__(self, equipe, i, j):
		self.equipe = equipe
		self.i = i
		self.j = j
		self.image = obtenir_image(f"image/roi_{self.equipe}.png")


	def cases_possibles(self, plateau):
		possibilites = [
			f'{self.i+1}{self.j}',
			f'{self.i+1}{self.j-1}',
			f'{self.i+1}{self.j+1}',
			f'{self.i}{self.j-1}',
			f'{self.i}{self.j+1}',
			f'{self.i-1}{self.j}',
			f'{self.i-1}{self.j-1}',
			f'{self.i-1}{self.j+1}',
		]

		for e in possibilites:
			if case_hors_plateau(e):
				possibilites.remove(e)
			else:
				if plateau[e] != None:
					possibilites.remove(e)

		return possibilites