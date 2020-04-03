import os
from tkinter import *
from tkinter import filedialog

from pypresence import Presence

from echec import *

class Fenetre(Tk): #L'idée et de créer une fenêtre sans brodures mais qui apparaissent tout de même dans la barre de tâches
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.little = Tk() #On crée une 2nd fenêtre qui n'est là que comme "bouton" dans la barre de tâches
		self.little.geometry("0x0") #On minimise sa taille
		self.little.lift(aboveThis=self) #On la positionne derrière la fenêtre principale
		self.little.bind("<Map>", self.apparition) #Lors de son apparition on fait appraître la fenêtre principale
		self.little.bind("<Unmap>", self.disparition) #Même chose pour la disparition
		self.little.protocol("WM_DELETE_WINDOW", self.quit) #Lors de sa fermeture on ferme la fenêtre principale
		self.overrideredirect(True) #On enlève les bordures de la fenêtre principale
		self.lift() #On la fait passer au premier plan
		self.attributes('-topmost', True) #On ajoute un attribut pour toujours la laisser au premier plan

		self.background_image = PhotoImage(file="images/fond.png")
		self.canvas = Canvas(self, border=0, highlightthickness=0, background="#303236", width=self.background_image.width(), height=self.background_image.height())
		self.canvas.grid(row=1, column=0)

		self.barre_outils = Frame(self, background="#292626")
		self.barre_outils.grid(row=0, column=0,)

		self.bouton_reduire = Button(self.barre_outils, width=3, height=1, bg="#292626", activebackground="#1f1c1c", text="-", font="Helvetica 10 bold", fg="white", activeforeground="white", border=0, relief=SUNKEN, command=self.little.iconify)
		self.bouton_reduire.grid(row=0, column=1)
		self.bouton_fermer = Button(self.barre_outils, width=3, height=1, bg="#960d03", activebackground="#6e0a02", text="x", font="Helvetica 10 bold", fg="white", activeforeground="white", border=0, relief=SUNKEN, command=self.quit)
		self.bouton_fermer.grid(row=0, column=2)
		self.barre_outils_vide = Canvas(self.barre_outils, width=self.background_image.width()-40-20, height=0, background=self.barre_outils["bg"], border=0, highlightthickness=0).grid(row=0, column=0)

		self.bouton_reduire.bind("<Enter>", self.entree_bouton)
		self.bouton_reduire.bind("<Leave>", self.sortie_bouton)
		self.bouton_fermer.bind("<Enter>", self.entree_bouton)
		self.bouton_fermer.bind("<Leave>", self.sortie_bouton)

		centrer_fenetre(self.little)
		centrer_fenetre(self)

		self.afficher_accueil()

		self.boutons_cases = {}
		self.affichage = {}
		self.affichage_id = {}
		self.affichage_id["popup"] = None
		self.couleur_case_noire = "black"
		self.couleur_case_blanche = "white"

		self.after(5000, self.connecter_rpc)

	def connecter_rpc(self):
		self.RPC = Presence('465805511930019852')
		self.RPC.connect()
		self.actualiser_rpc()
	def actualiser_rpc(self):
		if self.partie["type"] == "menu":
			self.RPC.update(details="Dans le menu", large_image="logo", large_text="https://paypal.me/KyloRen3600")
		else:
			def maj(s):
				a = list(s)
				a[0] = a[0].upper()
				return "".join(a)
			try:
				partie = self.partie['rpc_type']
				tour = self.partie['rpc_tour']
				joueur = self.partie['rpc_joueur']
				debut = self.partie['rpc_debut']
				debug = self.partie['rpc_debug']
			except:
				partie = self.partie['type']
				self.partie['rpc_type'] = self.partie['type']
				tour = self.partie['tour']
				self.partie['rpc_tour'] = self.partie['tour']
				joueur = self.partie['joueur']
				self.partie['rpc_joueur'] = self.partie['joueur']
				debug = False
				self.partie['rpc_debug'] = True
				self.partie['rpc_debut'] = int(self.partie["debut"] - self.partie["temps_enregistre"])

			if debug==False or partie != self.partie['type'] or tour != self.partie['tour'] or joueur != self.partie['joueur']:
				partie = self.partie['type']
				self.partie['rpc_type'] = self.partie['type']
				tour = self.partie['tour']
				self.partie['rpc_tour'] = self.partie['tour']
				joueur = self.partie['joueur']
				self.partie['rpc_joueur'] = self.partie['joueur']
				self.RPC.update(start=self.partie['rpc_debut'], details=f"Partie {maj(partie)}", state=f"Tour n°{tour}", large_image="logo", large_text="https://paypal.me/KyloRen3600", small_image=f"pion_{joueur}", small_text=f"Joueur {maj(joueur)}")

		self.after(5000, self.actualiser_rpc)

	def apparition(self, e):
		self.wm_deiconify()
		self.lift()
	def disparition(self, e):
		self.wm_withdraw()
		self.lift()

	def afficher_accueil(self):
		self.partie = {"type": "menu", "rpc": 0}
		self.bouton_fermer["command"] = self.quit
		self.canvas.create_image(0, 0, image=self.background_image, anchor=NW)
		font = "Helvetica 20"
		width = 20
		self.bouton_bg = "#1f1e1d"
		self.bouton_fg = "#e0deda"
		self.bouton_activebg = "#292826"
		self.bouton_activefg = "#737270"
		self.boutons = []
		self.boutons.append(Button(self, text="Nouvelle Partie", bg=self.bouton_bg, fg=self.bouton_fg, activebackground=self.bouton_activebg, activeforeground=self.bouton_activefg, width=width, font=font, command=self.ouvrir_nouvelle, border=0, relief=SUNKEN))
		self.boutons.append(Button(self, text="Charger une Partie", bg=self.bouton_bg, fg=self.bouton_fg, activebackground=self.bouton_activebg, activeforeground=self.bouton_activefg, width=width, font=font, command=self.ouvrir_charger, border=0, relief=SUNKEN))
		self.boutons.append(Button(self, text="Quitter", bg=self.bouton_bg, fg=self.bouton_fg, activebackground=self.bouton_activebg, activeforeground=self.bouton_activefg, width=width, font=font, command=self.little.quit, border=0, relief=SUNKEN))
		for bouton in self.boutons:
			bouton.bind("<Enter>", self.entree_bouton)
			bouton.bind("<Leave>", self.sortie_bouton)
		self.b1 = self.canvas.create_window(self.canvas.winfo_width()//2, self.canvas.winfo_height()//2-self.canvas.winfo_height()//5, window=self.boutons[0], anchor=CENTER)
		self.b2 = self.canvas.create_window(self.canvas.winfo_width()//2, self.canvas.winfo_height()//2, window=self.boutons[1], anchor=CENTER)
		self.b3 = self.canvas.create_window(self.canvas.winfo_width()//2, self.canvas.winfo_height()//2+self.canvas.winfo_height()//5, window=self.boutons[2], anchor=CENTER)


	def ouvrir_accueil(self):
		self.boutons[0]["text"] = "Nouvelle Partie"
		self.boutons[1]["text"] = "Charger une Partie"
		self.boutons[2]["text"] = "Quitter"
		self.boutons[0]["command"] = self.ouvrir_nouvelle
		self.boutons[1]["command"] = self.ouvrir_charger
		self.boutons[2]["command"] = self.little.quit

	def ouvrir_nouvelle(self):
		self.boutons[0]["text"] = "Partie Normale"
		self.boutons[1]["text"] = "Partie Blitz"
		self.boutons[2]["text"] = "Retour"
		self.boutons[0]["command"] = lambda: nouvelle_partie(self._root(), "normale")
		self.boutons[1]["command"] = lambda: nouvelle_partie(self._root(), "blitz")
		self.boutons[2]["command"] = self.ouvrir_accueil

	def ouvrir_charger(self):
		charger_partie(self, filedialog.askopenfilename(initialdir=os.getcwd()+"/parties", title="Choisissez une partie",
								   filetypes=[("Sauvegarde de partie", "*.json")]))

	def entree_bouton(self, e):
		e.widget["bg"] = e.widget["activebackground"]
	def sortie_bouton(self, e):
		color = None
		if e.widget == self.bouton_fermer:
			color = "#960d03"
		elif e.widget == self.bouton_reduire:
			color = "#292626"
		else:
			color = self.bouton_bg
		if color != None:
			e.widget["bg"] = color

def centrer_fenetre(fen):
	fen.update_idletasks()
	width = fen.winfo_width()
	height = fen.winfo_height()
	x = (fen.winfo_screenwidth() // 2) - (width // 2)
	y = (fen.winfo_screenheight() // 2) - (height // 2)
	fen.geometry('{}x{}+{}+{}'.format(width, height, x, y))

app = Fenetre()
app.little.title("Echec")
app.mainloop()