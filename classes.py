from tkinter import *
from fonctions import *

class Pion():
	def __init__(self, equipe, i, j):
		self.equipe = equipe
		self.i = i
		self.j = j
		self.deplace = False
		#self.image = PhotoImage(file=f"image/pion_{self.equipe}.png")
		self.image = obtenir_image(f"image/pion_{self.equipe}.png")
		
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
		print(len(possibilites))
		print((possibilites))
		i = 0
		for e in possibilites:
			print(e)
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
	







