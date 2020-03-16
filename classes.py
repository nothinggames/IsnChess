from tkinter import *

class Pion():
	def __init__(self, equipe, i, j):
		self.equipe = equipe
		self.i = i
		self.j = j
		self.image = PhotoImage(file="image/pion.png")
		
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


	def cases_possibles(self):
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

	
	def cases_possibles(self):
		pass

class Fou():
	def __init__(self, equipe, i, j):
		self.equipe = equipe
		self.i = i
		self.j = j
		self.image = None
	def cases_possibles(self):
		possibilites = []
	
	def cases_possibles(self):
		pass

class Dame():
	def __init__(self, equipe, i, j):
		self.equipe = equipe
		self.i = i
		self.j = j
		self.image = None

	
	def cases_possibles(self):
		pass

class Roi():
	def __init__(self, equipe, i, j):
		self.equipe = equipe
		self.i = i
		self.j = j
		self.image = None


	def cases_possibles(self):
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
	

#------------ C'est un exemple ou on garde?-------------
"""
pion = [
	[tour, cavaloer,],
	[pion, pio ],
	
]
pion[0][0]
"""
#------------ C'est un exemple ou on garde?-------------





