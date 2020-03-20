from tkinter import *

#Nouvelle partie
#Charger une partie
fen = Tk()
fen.overrideredirect(True)

positionRight = int(fen.winfo_screenwidth() / 3 - fen.winfo_reqwidth() / 2)
positionDown = int(fen.winfo_screenheight() / 3 - fen.winfo_reqheight() / 2)
fen.geometry("+{}+{}".format(positionRight, positionDown))


background = PhotoImage(file="background.png")

menu = Canvas(fen, border=-5, background="black", width=background.width(), height=background.height())
menu.create_image(0, 0, image=background, anchor=NW)
menu.pack(fill=BOTH)

fen.after(15000, menu.destroy)
fen.after(5000, lambda: fen.overrideredirect(False))
fen.mainloop()